"""
Application settings for the Notes API.

Loads configuration from environment variables or .env file.
"""

import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


class Settings:
    """Application settings with sensible defaults for development."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/notes.db")


# Singleton instance
settings = Settings()
