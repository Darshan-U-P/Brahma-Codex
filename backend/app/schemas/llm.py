from pydantic import BaseModel


class LLMStatusResponse(BaseModel):
    loaded: bool


class LLMActionResponse(BaseModel):
    success: bool
    loaded: bool
    message: str


class LLMInfoResponse(BaseModel):
    loaded: bool
    model_path: str
    model_exists: bool
    context_size: int
    gpu_layers: int