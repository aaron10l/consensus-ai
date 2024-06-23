import os
import re
import warnings
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import AnthropicBedrock
from botocore.exceptions import ClientError
import boto3
import json

load_dotenv()

def get_gpt_response(message_history):
	client = OpenAI(
    	api_key=os.getenv('GPT_KEY')
	)
	completion = client.chat.completions.create(
  		model="gpt-3.5-turbo",
  		messages=message_history
	)

	response = completion.choices[0].message.content
	return response

def get_llama_response(message_history):
	# Create a Bedrock Runtime client in the AWS Region of your choice.
	client = boto3.client("bedrock-runtime", 
					   aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
					   aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
					   region_name="us-east-1")

	# Set the model ID, e.g., Llama 3 8b Instruct.
	model_id = "meta.llama3-8b-instruct-v1:0"

	# Define the prompt for the model.
	# prompt = "Describe the purpose of a 'hello world' program in one line."

	# Embed the prompt in Llama 3's instruction format.
	formatted_prompt = f"""
	<|begin_of_text|>
	<|start_header_id|>user<|end_header_id|>
	{message_history}
	<|eot_id|>
	<|start_header_id|>assistant<|end_header_id|>
	"""

	# Format the request payload using the model's native structure.
	native_request = {
    	"prompt": formatted_prompt,
    	"max_gen_len": 512,
    	"temperature": 0.5,
	}

	# Convert the native request to JSON.
	request = json.dumps(native_request)

	try:
		# Invoke the model with the request.
		response = client.invoke_model(modelId=model_id, body=request)

	except (ClientError, Exception) as e:
		print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
		exit(1)

	# Decode the response body.
	model_response = json.loads(response["body"].read())

	# Extract and print the response text.
	response_text = model_response["generation"]

	if isinstance(response_text, list):
		return response_text[0]['content']
	return response_text

def get_claude_response(message_history):
    client = AnthropicBedrock(
        aws_access_key=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_key=os.getenv("AWS_SECRET_KEY"),
        aws_region="us-east-1",
    )

    # Filter out the system message and convert user/assistant messages
    claude_messages = []
    for msg in message_history:
        if msg["role"] == "system":
            continue
        if not claude_messages or claude_messages[-1]["role"] != msg["role"]:
            claude_messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})
        else:
            # If the roles are the same, combine the content
            claude_messages[-1]["content"] += f"\n\n{msg['content']}"

    # If there's a system message, prepend it to the first user message
    system_message = next((msg["content"] for msg in message_history if msg["role"] == "system"), None)
    if system_message and claude_messages:
        claude_messages[0]["content"] = f"{system_message}\n\n{claude_messages[0]['content']}"

    # Ensure the messages start with a user message
    if claude_messages and claude_messages[0]["role"] != "user":
        claude_messages.insert(0, {"role": "user", "content": "Hello"})

    message = client.messages.create(
        model="anthropic.claude-3-5-sonnet-20240620-v1:0",
        max_tokens=256,
        messages=claude_messages
    )
    return message.content[0].text

def parse_llm_response(response):
	"""
	Parses the response given by the LLM to determine what number response is the winner.
	"""
	winner = None
	try:
		winner = int(response)
	except:
		pattern = r'[.,\s;]+'
		words = re.split(pattern, response)
		for word in words:
			try:
				winner = int(word)
				return winner
			except:
				continue
	if not winner:
		warnings.warn("no valid integer was found in the llms response. default is 1")
		print("response: {response}")
		return 1
	else:
		return winner
	