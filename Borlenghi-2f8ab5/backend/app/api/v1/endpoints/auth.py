from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, Token
from app.core.security import create_access_token

router = APIRouter()

# Hardcoded user for the challenge (as per spec)
DEMO_USER: dict[str, str] = {"username": "admin", "password": "admin"}


@router.post("/login", response_model=Token)
def login(data: LoginRequest) -> Token:
    if data.username != DEMO_USER["username"] or data.password != DEMO_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token: str = create_access_token(data={"sub": data.username})
    return Token(access_token=token)
