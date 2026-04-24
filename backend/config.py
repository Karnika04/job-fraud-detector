import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Correct PostgreSQL connection
    database_url: AnyUrl | str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/jobfraud",
    )

    model_path: str = os.getenv("MODEL_PATH", "models/job_fraud_model.pkl")
    vectorizer_path: str = os.getenv("VECTORIZER_PATH", "models/tfidf_vectorizer.pkl")

    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()