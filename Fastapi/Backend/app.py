from fastapi import FastAPI, HTTPException, status, Depends # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore
import secrets
import ollama   # <-- NEW

app = FastAPI(title="FastAPI + Token + Ollama")

# Store token in memory
CURRENT_TOKEN = None
security = HTTPBearer()

# -------------------------------
# Generate Token
# -------------------------------
@app.post("/generate-token")
def generate_token():
    global CURRENT_TOKEN
    CURRENT_TOKEN = secrets.token_hex(32)
    return {"token": CURRENT_TOKEN}


# -------------------------------
# Token Validator
# -------------------------------
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    global CURRENT_TOKEN
    if CURRENT_TOKEN is None:
        raise HTTPException(status_code=400, detail="Generate token first.")
    if credentials.credentials != CURRENT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return True


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
