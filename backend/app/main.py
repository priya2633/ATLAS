from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    logger.info("Starting Atlas...")

    yield

    logger.info("Shutting down Atlas...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/")
async def root():
    logger.info("Root endpoint called.")

    return {
        "message": "Welcome to Atlas 🚀"
    }


@app.get("/health")
async def health():
    logger.info("Health check successful.")

    return {
        "status": "healthy"
    }