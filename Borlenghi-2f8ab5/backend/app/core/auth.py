"""
FastAPI dependency for protecting routes with JWT authentication.

Provides get_current_user dependency that extracts and validates the
Bearer token from the Authorization header.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_token

# OAuth2 scheme expecting Bearer token from /api/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    FastAPI dependency that validates the JWT token and returns the username.

    Usage in endpoints:
        @router.get("/protected")
        def protected_route(username: str = Depends(get_current_user)):
            return {"user": username}

    Args:
        token: Bearer token extracted from Authorization header.

    Returns:
        The username (sub claim) from the token.

    Raises:
        HTTPException 401: If token is invalid or expired.
    """
    username: str | None = verify_token(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username
