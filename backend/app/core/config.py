from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

# backend/app/core/config.py
# Go up to the backend directory.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Go up one more level to the Local Codex project root.
PROJECT_ROOT = BASE_DIR.parent


# --------------------------------------------------
# Application Settings
# --------------------------------------------------

class Settings(BaseSettings):
    """Application configuration settings."""

    # Application
    APP_NAME: str = "Local Codex"
    APP_VERSION: str = "0.1.0"

    # --------------------------------------------------
    # Local LLM
    # --------------------------------------------------

    MODEL_PATH: str = str(
        PROJECT_ROOT
        / "models"
        / "qwen2.5-coder-7b-instruct-q4_k_m.gguf"
    )

    MODEL_CONTEXT_SIZE: int = 8192

    MODEL_GPU_LAYERS: int = 0

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_PATH: str = str(
        BASE_DIR / "local_codex.db"
    )

    # --------------------------------------------------
    # Project Workspaces
    # --------------------------------------------------

    WORKSPACE_ROOT: str = str(
        PROJECT_ROOT / "workspace"
    )

    # --------------------------------------------------
    # Environment Configuration
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


# --------------------------------------------------
# Global Settings Instance
# --------------------------------------------------

settings = Settings()