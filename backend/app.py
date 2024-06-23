from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from llms import parse_llm_response, get_gpt_response, get_llama_response, get_claude_response
import asyncio

app = Flask(__name__)
CORS(app)

# global chat history
message_history = [{"role": "system", "content": "You are a helpful assistant."}]

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

@app.route('/get-responses', methods=['POST'])
async def get_responses():
    data = request.json
    prompt = data['prompt']
    message_history.append({"role": "user", "content": prompt})
    
    # Get initial responses in parallel
    responses = await asyncio.gather(
        get_gpt_response(message_history),
        get_llama_response(message_history),
        get_claude_response(message_history)
    )
    
    responses = {
        'GPT': responses[0],
        'LLaMa': responses[1],
        'Claude': responses[2]
    }
    
    # Collect votes
    votes = {'GPT': 0, 'LLaMa': 0, 'Claude': 0}

    # model and numbering:
    numbered_models = {
        1: 'GPT',
        2: 'LLaMa',
        3: 'Claude'
    }

    print(f"Prompt: {prompt}")
    print("Responses:")
    for number, model in numbered_models.items():
        print(f"{number}. {responses[model]}")
    
    async def get_vote(model_name):
        temp_chat_history = message_history.copy()[:-1]
        temp_chat_history.pop()
        combined_prompt = f"{prompt}\n\nResponses:\n1. {responses['GPT']}\n2. {responses['LLaMa']}\n3. {responses['Claude']}\n\nWhich is the best response? Respond with the response number."
 
        temp_chat_history.append({"role": "user", "content": combined_prompt})

        if model_name == 'GPT':
            vote = parse_llm_response(await get_gpt_response(temp_chat_history))
        elif model_name == 'LLaMa':
            vote = parse_llm_response(await get_llama_response(temp_chat_history))
        elif model_name == 'Claude':
            vote = parse_llm_response(await get_claude_response(temp_chat_history))

        return numbered_models[vote]

    vote_results = await asyncio.gather(*[get_vote(model) for model in responses.keys()])
    for vote in vote_results:
        votes[vote] += 1
    
    # Determine the winner
    winner = max(votes, key=votes.get)

    message_history.append({'role': 'assistant', 'content': responses[winner]})
    return jsonify({'winner': winner, 'response': responses[winner]})

if __name__ == '__main__':
    app.run(debug=True)