"""
Centralized logging configuration for Atlas.

This module configures Loguru as the single logging backend for the
entire application while intercepting Python's standard logging module
(Uvicorn, FastAPI, SQLAlchemy, etc.).

Features
--------
- Colored console logs for development
- Structured JSON logs for production
- Log rotation & retention
- Thread-safe logging
- Standard logging interception
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

# =============================================================================
# Constants
# =============================================================================

LOG_DIR = Path("logs")

INTERCEPT_LOGGERS = (
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "fastapi",
    "sqlalchemy",
)

# =============================================================================
# Loguru Intercept Handler
# =============================================================================


class InterceptHandler(logging.Handler):
    """
    Redirects Python's standard logging records to Loguru.

    This ensures that logs emitted by third-party libraries
    (FastAPI, SQLAlchemy, Uvicorn, etc.) all use Atlas'
    centralized logging configuration.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = logging.currentframe()
        depth = 2

        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


# =============================================================================
# Logger Configuration
# =============================================================================


def configure_logging() -> None:
    """
    Configure Atlas logging.

    This should be called once during application startup.

    Creates:
        - Colored console logs for developers
        - JSON structured logs for production
        - Intercepts Python standard logging
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.remove()

    # -------------------------------------------------------------------------
    # Console Logs (Development)
    # -------------------------------------------------------------------------

    logger.add(
        sys.stdout,
        level=settings.log_level,
        colorize=True,
        enqueue=True,
        backtrace=settings.debug,
        diagnose=False,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # -------------------------------------------------------------------------
    # Structured JSON Logs (Production)
    # -------------------------------------------------------------------------

    logger.add(
        LOG_DIR / "atlas.json",
        level=settings.log_level,
        serialize=True,
        enqueue=True,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=settings.debug,
        diagnose=False,
    )

    # -------------------------------------------------------------------------
    # Intercept Standard Logging
    # -------------------------------------------------------------------------

    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=logging.NOTSET,
        force=True,
    )

    for logger_name in INTERCEPT_LOGGERS:
        intercepted_logger = logging.getLogger(logger_name)
        intercepted_logger.handlers = [InterceptHandler()]
        intercepted_logger.propagate = False

    logger.info("Logging successfully configured.")


# =============================================================================
# Public Logger
# =============================================================================

__all__ = [
    "logger",
    "configure_logging",
]