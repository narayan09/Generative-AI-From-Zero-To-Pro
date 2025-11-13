from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
import subprocess
import os

# ---------------- Logging Setup ----------------
LOG_FILE = "app.log"

# Create log directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),  # Save to file
        # logging.StreamHandler()  # Uncomment if you also want logs in console
    ]
)
logger = logging.getLogger("ai_backend")
# ------------------------------------------------

app = FastAPI()

# Allow frontend (Streamlit) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins for dev, restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class Prompt(BaseModel):
    message: str

# Function to call Ollama model
def call_ollama(message: str):
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3:mini", message],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.error(f"Ollama returned error: {result.stderr.strip()}")
            return f"Error from Ollama: {result.stderr.strip()}"
    except Exception as e:
        logger.exception("Error calling Ollama")
        return str(e)

# FastAPI route
@app.post("/chat")
async def chat(prompt: Prompt, request: Request):
    client_ip = request.client.host
    logger.info(f"Request from {client_ip}: {prompt.message[:80]}...")

    try:
        response = call_ollama(prompt.message)
        logger.info(f"Response successfully generated for {client_ip}")
        return {"response": response}
    except Exception as e:
        logger.exception(f"Error processing request from {client_ip}")
        return {"error": str(e)}
