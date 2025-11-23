from fastapi import Depends, HTTPException # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore

security = HTTPBearer()
CURRENT_TOKEN = None

def set_token(token: str):
    global CURRENT_TOKEN
    CURRENT_TOKEN = token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    global CURRENT_TOKEN
    if CURRENT_TOKEN is None:
        raise HTTPException(status_code=400, detail="Generate token first.")
    if credentials.credentials != CURRENT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return True
