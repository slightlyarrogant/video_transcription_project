from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv, find_dotenv

openai_client = None
anthropic_client = None

def init_clients():
    global openai_client, anthropic_client
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        print(f"Summarization: Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path, override=True)
    else:
        print("Summarization: No .env file found!")

    openai_api_key = os.getenv("OPENAI_API_KEY", "Not found")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "Not found")
    
    print(f"Summarization: Using OpenAI API key (first 5 chars): {openai_api_key[:5]}...")
    print(f"Summarization: Using Anthropic API key (first 5 chars): {anthropic_api_key[:5]}...")
    
    openai_client = OpenAI(api_key=openai_api_key)
    anthropic_client = Anthropic(api_key=anthropic_api_key)

def summarize_text(text, config, title=None):
    global openai_client, anthropic_client
    if openai_client is None or anthropic_client is None:
        init_clients()

    model = config['summarization']['model']
    max_tokens = config['summarization']['max_summary_length']

    prompt = config['summarization']['prompt']['user'].format(text=text, title=title)

    if model.startswith("gpt"):
        messages = [
            {"role": "system", "content": config['summarization']['prompt']['system']},
            {"role": "user", "content": prompt}
        ]
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    elif model.startswith("claude"):
        response = anthropic_client.completions.create(
            model=model,
            max_tokens_to_sample=max_tokens,
            prompt=f"{config['summarization']['prompt']['system']}\n\nHuman: {prompt}\n\nAssistant:",
        )
        return response.completion
    
    else:
        raise ValueError(f"Unsupported model: {model}")
