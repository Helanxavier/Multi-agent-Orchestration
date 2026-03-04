import os
import requests
from dotenv import load_dotenv

load_dotenv()

def verify_groq_key():
    key = os.getenv("GROQ_API_KEY")
    print(f"Key: {key[:8]}...{key[-4:]}")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_groq_key()
