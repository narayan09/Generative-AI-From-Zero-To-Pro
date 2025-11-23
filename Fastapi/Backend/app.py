from fastapi import FastAPI, HTTPException, status, Depends # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore
import secrets
import ollama   # <-- NEW
from auth import set_token
from open_router import router
from auth import verify_token

app = FastAPI()
app.include_router(router)

@app.post("/generate-token")
def generate_token():
    import secrets
    token = secrets.token_hex(32)
    set_token(token)
    return {"token": token}




# -------------------------------
# Protected Route: Ask Ollama
# -------------------------------
@app.post("/ask-ollama")
def ask_ollama(request: dict, _: bool = Depends(verify_token)):
    prompt = request.get("prompt")
    model = request.get("model", "phi3:mini")  # default model
    token_limit = request.get("token_limit", 100)  # default: 100 tokens

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    try:
        # Call Ollama model
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "num_predict": token_limit
            }
        )
        return {"response": response["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
