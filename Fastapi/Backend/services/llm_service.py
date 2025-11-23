from langsmith import traceable
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

@traceable  # This enables tracing for LangSmith
def generate_llm_response(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt}
    )
    return response.json().get("response", "No response")
