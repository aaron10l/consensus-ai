import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_gpt_response(prompt):
	print(f"prompt: {prompt}")

	client = OpenAI(
    	api_key=os.getenv('GPT_KEY')
	)
	
	completion = client.chat.completions.create(
  		model="gpt-3.5-turbo",
  		messages=[
    		{"role": "user", "content": prompt}
  		]
	)

	response = completion.choices[0].message.content
	return response

def get_llama_response(prompt):
	return "llama response"

def get_claude_response(prompt):
	return "claude RESPONSE"

