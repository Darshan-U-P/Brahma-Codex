import logging
from functools import lru_cache
from pathlib import Path
from typing import Generator

from llama_cpp import Llama

from app.core.config import settings
from app.core.exceptions import (
    LLMGenerationError,
    ModelLoadError,
)


logger = logging.getLogger(__name__)


class LlamaClient:
    def __init__(self):
        self.llm: Llama | None = None

    def load_model(self) -> bool:
        """Load the GGUF model into memory."""
        if self.llm is not None:
            logger.info("Model is already loaded.")
            return False

        model_path = Path(settings.MODEL_PATH).resolve()

        if not model_path.exists():
            logger.error("Model not found: %s", model_path)

            raise ModelLoadError(
                f"Model not found: {model_path}"
            )

        try:
            logger.info(
                "Loading model from: %s",
                model_path,
            )

            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=settings.MODEL_CONTEXT_SIZE,
                n_gpu_layers=settings.MODEL_GPU_LAYERS,
                verbose=True,
            )

            logger.info("Model loaded successfully.")

            return True

        except Exception as error:
            logger.exception(
                "Failed to load model."
            )

            self.llm = None

            raise ModelLoadError(
                f"Failed to load model: {str(error)}"
            ) from error

    def unload_model(self) -> bool:
        """Unload the model from memory."""
        if self.llm is None:
            logger.info("Model is not loaded.")
            return False

        try:
            logger.info("Unloading model...")

            self.llm.close()
            self.llm = None

            logger.info(
                "Model unloaded successfully."
            )

            return True

        except Exception as error:
            logger.exception(
                "Failed to unload model."
            )

            raise ModelLoadError(
                f"Failed to unload model: {str(error)}"
            ) from error

    def is_loaded(self) -> bool:
        """Check whether the model is loaded."""
        return self.llm is not None

    def get_info(self) -> dict:
        """Return model configuration information."""
        model_path = Path(
            settings.MODEL_PATH
        ).resolve()

        return {
            "loaded": self.is_loaded(),
            "model_path": str(model_path),
            "model_exists": model_path.exists(),
            "context_size": settings.MODEL_CONTEXT_SIZE,
            "gpu_layers": settings.MODEL_GPU_LAYERS,
        }

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        """Generate a complete chat response."""
        try:
            if self.llm is None:
                self.load_model()

            logger.info(
                "Generating chat response."
            )

            return self.llm.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except ModelLoadError:
            raise

        except Exception as error:
            logger.exception(
                "LLM generation failed."
            )

            raise LLMGenerationError(
                f"LLM generation failed: {str(error)}"
            ) from error

    def chat_stream(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Generator:
        """Generate a streaming chat response."""
        try:
            if self.llm is None:
                self.load_model()

            logger.info(
                "Starting streaming generation."
            )

            stream = self.llm.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            for chunk in stream:
                yield chunk

            logger.info(
                "Streaming generation completed."
            )

        except ModelLoadError:
            raise

        except Exception as error:
            logger.exception(
                "Streaming generation failed."
            )

            raise LLMGenerationError(
                f"Streaming generation failed: {str(error)}"
            ) from error


@lru_cache
def get_llama_client() -> LlamaClient:
    """Return the shared LlamaClient instance."""
    return LlamaClient()