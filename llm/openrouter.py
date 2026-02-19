import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME

def call_openrouter_deepseek(prompt: str) -> str:
    """
    Calls DeepSeek R1 via OpenRouter.
    Returns response text or raises Exception on failure.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", # Optional
        "X-Title": "ClauseAI", # Optional
    }
    
    data = {
        "model": OPENROUTER_MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=10  # Reduced timeout for faster fallback
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"Empty response from OpenRouter: {result}")
        else:
            raise Exception(f"OpenRouter Error {response.status_code}: {response.text}")
            
    except Exception as e:
        raise Exception(f"DeepSeek call failed: {str(e)}")
