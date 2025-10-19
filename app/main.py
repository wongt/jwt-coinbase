import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Coinbase CDP JWT helper (present in your wongt/python-cdp-sdk base image)
from cdp.auth.utils.jwt import generate_jwt, JwtOptions

app = FastAPI(title="JWT Generator (Coinbase)", version="1.0.0")

API_KEY_ID = os.getenv("COINBASE_API_KEY_ID")
API_KEY_SECRET = os.getenv("COINBASE_API_KEY_SECRET")  # PEM with BEGIN/END + newlines

class TokenRequest(BaseModel):
    request_domain: str = Field(default="https://api.coinbase.com")
    request_method: str = Field(default="GET")
    request_path: str
    expires_in: int = Field(default=120, ge=30, le=300)

class TokenResponse(BaseModel):
    jwt: str
    request_method: str
    request_path: str
    date: str

@app.post("/token", response_model=TokenResponse)
def create_token(body: TokenRequest):
    if not API_KEY_ID or not API_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Missing API credentials")

    try:
        jwt_token = generate_jwt(JwtOptions(
            api_key_id=API_KEY_ID,
            api_key_secret=API_KEY_SECRET,
            request_method=body.request_method,
            request_host=body.request_domain,
            request_path=body.request_path,
            expires_in=body.expires_in
        ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JWT generation failed: {e}")

    return TokenResponse(
        jwt=jwt_token,
        request_method=body.request_method,
        request_path=body.request_path,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.get("/healthz")
def health():
    return {"status": "ok"}
