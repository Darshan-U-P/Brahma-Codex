import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.llm import router as llm_router
from app.core.config import settings
from app.core.exceptions import LocalCodexError
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description="Local LLM-powered software development platform",
    version=settings.APP_VERSION,
)


@app.exception_handler(LocalCodexError)
async def local_codex_exception_handler(
    request: Request,
    exc: LocalCodexError,
):
    logger.error(
        "Local Codex error on %s: %s",
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
        },
    )


app.include_router(health_router)
app.include_router(llm_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} backend is running",
        "version": settings.APP_VERSION,
    }