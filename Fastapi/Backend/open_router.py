import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI # type: ignore
from fastapi import APIRouter, HTTPException, Depends # type: ignore
from auth import verify_token
from langsmith import traceable

load_dotenv()
router = APIRouter()   # <-- IMPORTANT

class OpenRouterConfig:

    MODELS = {
        "gpt-4": "openai/gpt-4-turbo",
        "gpt-3.5": "openai/gpt-3.5-turbo",
        "claude-3": "anthropic/claude-3-sonnet",
        "claude-3.5": "anthropic/claude-3.5-sonnet",
        "gemini": "google/gemini-pro",
        "llama-3": "meta-llama/llama-3-70b-instruct",
        "mistral": "mistralai/mistral-7b-instruct"
    }

    @staticmethod
    def get_model(model_name="x-ai/grok-4.1-fast:free", temperature=0.7):
        return ChatOpenAI(
            model=OpenRouterConfig.MODELS.get(model_name, "x-ai/grok-4.1-fast:free"),
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "LangChain Practice Project"
            },
            temperature=temperature
        )

@router.post("/ask_prompt")   # <-- now this becomes part of router
@traceable
def ask_prompt(request: dict, _: bool = Depends(verify_token)):
    prompt = request.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    try:
        llm = OpenRouterConfig.get_model()
        response = llm.invoke(prompt)
        return {"response": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
