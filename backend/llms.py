import os
import re
import warnings
from dotenv import load_dotenv
from openai import OpenAI

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
	return "LLAMA response"

def get_claude_response(message_history):
	return "claude RESPONSE"

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
		return 0
	else:
		return winner
	