import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _bool(key: str, default: str = "false") -> bool:
    return os.getenv(key, default).lower() in ("true", "1", "yes")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    if not SECRET_KEY or not JWT_SECRET_KEY:
        raise ValueError(
            "SECRET_KEY and JWT_SECRET_KEY must be set in environment variables"
        )

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///citypulse.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # ── Feature Toggles ──────────────────────────────────────────────
    # Set to "false" / "0" / "no" to disable any service in MVP / testing.
    EMAIL_ENABLED = _bool("EMAIL_ENABLED", "false")
    SMS_ENABLED = _bool("SMS_ENABLED", "false")
    S3_ENABLED = _bool("S3_ENABLED", "true")
    IMAGE_CLASSIFICATION_ENABLED = _bool("IMAGE_CLASSIFICATION_ENABLED", "false")
    AI_TEXT_ENABLED = _bool("AI_TEXT_ENABLED", "false")
    GEOCODING_ENABLED = _bool("GEOCODING_ENABLED", "true")

    # ── S3 ───────────────────────────────────────────────────────────
    S3_CONFIG = {
        "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "aws_access_key_id": os.getenv("S3_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("S3_SECRET_ACCESS_KEY"),
        "bucket_name": os.getenv("S3_BUCKET_NAME"),
        "region_name": os.getenv("S3_REGION_NAME"),
    }

    # ── Mail (Flask-Mail) ────────────────────────────────────────────
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@citypulse.com")

    # ── Ollama (local LLM) ──────────────────────────────────────────
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # ── Ollama Vision Model (image classification) ──────────────────
    OLLAMA_VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "gemma4:31b-cloud")
    OLLAMA_VISION_CONFIDENCE = float(os.getenv("OLLAMA_VISION_CONFIDENCE", "0.3"))
