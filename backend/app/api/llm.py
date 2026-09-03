from fastapi import APIRouter

from app.llm.client import get_llama_client
from app.schemas.llm import (
    LLMActionResponse,
    LLMInfoResponse,
    LLMStatusResponse,
)


router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.get(
    "/status",
    response_model=LLMStatusResponse,
)
async def llm_status() -> LLMStatusResponse:
    client = get_llama_client()

    return LLMStatusResponse(
        loaded=client.is_loaded()
    )


@router.post(
    "/load",
    response_model=LLMActionResponse,
)
async def load_model() -> LLMActionResponse:
    client = get_llama_client()

    was_loaded = client.load_model()

    return LLMActionResponse(
        success=True,
        loaded=True,
        message=(
            "Model loaded successfully."
            if was_loaded
            else "Model is already loaded."
        ),
    )


@router.post(
    "/unload",
    response_model=LLMActionResponse,
)
async def unload_model() -> LLMActionResponse:
    client = get_llama_client()

    was_unloaded = client.unload_model()

    return LLMActionResponse(
        success=True,
        loaded=False,
        message=(
            "Model unloaded successfully."
            if was_unloaded
            else "Model was not loaded."
        ),
    )


@router.get(
    "/info",
    response_model=LLMInfoResponse,
)
async def llm_info() -> LLMInfoResponse:
    client = get_llama_client()

    return LLMInfoResponse(
        **client.get_info()
    )