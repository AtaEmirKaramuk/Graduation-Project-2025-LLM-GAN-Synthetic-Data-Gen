import requests
import json
import time

import requests
import json

API_URL = "https://api.openai.com/v1/chat/completions"

def query_LLM(prompt: str, api_key: str, model="gpt-4o-mini", temperature=0.7, max_tokens=1024):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"OpenAI API error {response.status_code}: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]

"""
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_LLM(prompt: str, api_key: str, model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.7, max_tokens=512):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]

"""


"""API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/LLM-7b-beta"

def query_LLM(prompt, api_key, max_new_tokens=512, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": True
        }
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    result = response.json()
    return result[0]["generated_text"] if isinstance(result, list) else result["generated_text"]
"""