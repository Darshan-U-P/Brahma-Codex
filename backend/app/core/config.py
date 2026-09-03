from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    APP_NAME: str = "Local Codex"
    APP_VERSION: str = "0.1.0"

    MODEL_PATH: str = str(
        PROJECT_ROOT
        / "models"
        / "qwen2.5-coder-7b-instruct-q4_k_m.gguf"
    )

    MODEL_CONTEXT_SIZE: int = 8192
    MODEL_GPU_LAYERS: int = 0

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()