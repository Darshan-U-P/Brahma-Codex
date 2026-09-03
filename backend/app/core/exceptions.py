class LocalCodexError(Exception):
    """Base exception for Local Codex."""
    pass


class ModelNotLoadedError(LocalCodexError):
    """Raised when the model is not loaded."""
    pass


class ModelLoadError(LocalCodexError):
    """Raised when the model fails to load."""
    pass


class LLMGenerationError(LocalCodexError):
    """Raised when text generation fails."""
    pass