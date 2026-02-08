from fastapi import Header, HTTPException, status
import os

API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise RuntimeError("Ah you ain't got the API key configured")
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key not recognized",
        )