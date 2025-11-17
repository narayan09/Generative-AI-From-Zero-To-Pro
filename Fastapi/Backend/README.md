# 🚀 FastAPI + Ollama Backend

This backend provides:
- Token-based authentication  
- Token generation from Swagger UI  
- Secure API that sends prompts to the Ollama LLM  
- Works with the Streamlit frontend

---
## uvicorn app:app --reload

## 📁 Project Structure

app.py

🧪 Example Request (Swagger UI)
{
  "prompt": "Write a detailed explanation of AI.",
  "model": "llama3",
  "token_limit": 50
}

