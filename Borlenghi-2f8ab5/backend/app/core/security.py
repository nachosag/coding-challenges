"""
JWT token creation and verification utilities.

Uses PyJWT to encode/decode tokens with the configured SECRET_KEY and ALGORITHM.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt

from app.core.config import settings


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode. Must contain 'sub' claim (username).
        expires_delta: Optional custom expiration time.
            Defaults to ACCESS_TOKEN_EXPIRE_MINUTES from settings.

    Returns:
        Encoded JWT string.
    """
    to_encode: dict[str, Any] = data.copy()

    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode( # pyright: ignore[reportUnknownMemberType]
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Decode and validate a JWT token.

    Args:
        token: The JWT string to verify.

    Returns:
        The 'sub' claim (username) if valid, None if decoding fails.
    """
    try:
        payload: Any = jwt.decode( # pyright: ignore[reportUnknownMemberType]
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")
        return username
    except jwt.PyJWTError:
        return None
