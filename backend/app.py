from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from llms import parse_llm_response, get_gpt_response, get_llama_response, get_claude_response

app = Flask(__name__)
CORS(app)

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
    
    # Get initial responses
    gpt_response = get_gpt_response(prompt)
    llama_response = get_llama_response(prompt)
    claude_response = get_claude_response(prompt)
    
    responses = {
        'GPT': gpt_response,
        'LLaMa': llama_response,
        'Claude': claude_response
    }
    
    # Collect votes
    votes = {'GPT': 0, 'LLaMa': 0, 'Claude': 0}

    # model and numbering:
    numbered_models = {
        0: 'GPT',
        1: 'LLaMa',
        2: 'Claude'
    }
    
    for model_name, model_response in responses.items():
        combined_prompt = f"Original prompt: {prompt}\n\nResponses:\n1. {gpt_response}\n2. {llama_response}\n3. {claude_response}\n\nWhich is the best response? Respond with the response number."
        if model_name == 'GPT':
            vote = parse_llm_response(get_gpt_response(combined_prompt))
        elif model_name == 'LLaMa':
            vote = parse_llm_response(get_llama_response(combined_prompt))
        elif model_name == 'Claude':
            vote = parse_llm_response(get_claude_response(combined_prompt))

        votes[numbered_models[vote]] += 1
    
    # Determine the winner
    winner = max(votes, key=votes.get)
    print("--------------------------------------------------------------------------")
    print(f"prompt: {combined_prompt}")
    print(f"winning response: {responses[winner]}")
    
    return jsonify({'winner': winner, 'response': responses[winner]})

if __name__ == '__main__':
    app.run(debug=True)