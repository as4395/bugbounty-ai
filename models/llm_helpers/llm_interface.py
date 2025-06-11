# Purpose:
#   Provides a clean interface for interacting with OpenAI's GPT models.

import openai
import yaml

def load_openai_config(path='configs/openai_config.yaml'):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config.get('OpenAI_API_Key'), config.get('model', 'gpt-4')

class LLMHelper:
    def __init__(self):
        api_key, model = load_openai_config()
        if not api_key:
            raise ValueError("OpenAI API key not found in config.")
        openai.api_key = api_key
        self.model = model

    def chat_completion(self, messages, temperature=0.7):
        print("[LLM] Sending chat prompt to OpenAI...")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response['choices'][0]['message']['content'].strip()

    def complete(self, prompt, max_tokens=500, temperature=0.7):
        print("[LLM] Sending text prompt to OpenAI...")
        response = openai.Completion.create(
            model=self.model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response['choices'][0]['text'].strip()
