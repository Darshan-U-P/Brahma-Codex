import json
from typing import Iterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.llm.client import get_llama_client
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """Generate a complete response."""

    client = get_llama_client()

    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": request.message,
            }
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return ChatResponse(
        response=response["choices"][0]["message"]["content"]
    )


@router.post("/stream")
def chat_stream(request: ChatRequest):
    """Generate a streaming response using Server-Sent Events."""

    def generate() -> Iterator[str]:
        try:
            client = get_llama_client()

            stream = client.chat_stream(
                messages=[
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            for chunk in stream:
                choices = chunk.get("choices", [])

                if not choices:
                    continue

                delta = choices[0].get("delta", {})
                content = delta.get("content")

                if content:
                    data = json.dumps(
                        {"token": content},
                        ensure_ascii=False,
                    )

                    yield f"data: {data}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as error:
            error_data = json.dumps(
                {"error": str(error)}
            )

            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )