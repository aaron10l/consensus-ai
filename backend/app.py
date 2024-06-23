from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from llms import parse_llm_response, get_gpt_response, get_llama_response, get_claude_response

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
def get_responses():
    data = request.json
    prompt = data['prompt']
    message_history.append({"role": "user", "content": prompt})
    
    # Get initial responses
    gpt_response = get_gpt_response(message_history)
    llama_response = get_llama_response(message_history)
    claude_response = get_claude_response(message_history)
    
    responses = {
        'GPT': gpt_response,
        'LLaMa': llama_response,
        'Claude': claude_response
    }
    
    # Collect votes
    votes = {'GPT': 0, 'LLaMa': 0, 'Claude': 0}

    # model and numbering:
    numbered_models = {
        1: 'GPT',
        2: 'LLaMa',
        3: 'Claude'
    }
    
    for model_name, model_response in responses.items():
        temp_chat_history = message_history.copy()[:-1]
        temp_chat_history.pop()
        combined_prompt = f"{prompt}\n\nResponses:\n1. {gpt_response}\n2. {llama_response}\n3. {claude_response}\n\nWhich is the best response? Respond with the response number."

        temp_chat_history.append({"role": "user", "content": combined_prompt})

        if model_name == 'GPT':
            vote = parse_llm_response(get_gpt_response(temp_chat_history))
        elif model_name == 'LLaMa':
            vote = parse_llm_response(get_llama_response(temp_chat_history))
        elif model_name == 'Claude':
            vote = parse_llm_response(get_claude_response(temp_chat_history))

        votes[numbered_models[vote]] += 1
    
    # Determine the winner
    winner = max(votes, key=votes.get)

    message_history.append({'role': 'assistant', 'content': responses[winner]})
    return jsonify({'winner': winner, 'response': responses[winner]})

if __name__ == '__main__':
    app.run(debug=True)