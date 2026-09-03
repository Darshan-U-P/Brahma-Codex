import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.agent import router as agent_router
from app.api.chat import router as chat_router
from app.api.files import router as files_router
from app.api.health import router as health_router
from app.api.llm import router as llm_router
from app.api.projects import router as projects_router

from app.core.config import settings
from app.core.exceptions import LocalCodexError
from app.core.logging import setup_logging

from app.database.init_db import init_db


# ============================================================
# Setup Logging
# ============================================================

setup_logging()

logger = logging.getLogger(__name__)


# ============================================================
# Create FastAPI Application
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    description="Local LLM-powered software development platform",
    version=settings.APP_VERSION,
)


# ============================================================
# Exception Handlers
# ============================================================

@app.exception_handler(LocalCodexError)
async def local_codex_exception_handler(
    request: Request,
    exc: LocalCodexError,
):
    """Handle Local Codex application errors."""

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


# ============================================================
# Application Startup
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize application resources."""

    init_db()

    logger.info(
        "Database initialized successfully."
    )


# ============================================================
# API Routers
# ============================================================

app.include_router(health_router)
app.include_router(llm_router)
app.include_router(chat_router)
app.include_router(projects_router)
app.include_router(files_router)
app.include_router(agent_router)


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
async def root():
    """Root endpoint."""

    return {
        "message": (
            f"{settings.APP_NAME} backend is running"
        ),
        "version": settings.APP_VERSION,
    }