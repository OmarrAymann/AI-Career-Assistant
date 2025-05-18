import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def ask_llm(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "do_sample": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Handle result depending on what format we receive
        if isinstance(result, list):
            item = result[0]
            if isinstance(item, dict) and "generated_text" in item:
                return item["generated_text"].strip()
            elif isinstance(item, str):
                return item.strip()
            else:
                return json.dumps(result)
        else:
            return json.dumps(result)

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except Exception as e:
        return f"Unhandled error: {e}"