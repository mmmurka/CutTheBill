"""aiogram_logging.py

Unified logging configuration for aiogram bots based on **loguru**.

Call :func:`setup_logging` as early as possible in your bot's entry‑point
(before importing heavy aiogram sub‑modules) to ensure that **all** standard
`logging` calls (including those coming from `aiogram` itself) are routed
through *loguru* with a consistent, coloured output and optional file
rotation.

The behaviour mimics the logger you provided for a FastAPI app but is
extended to cover common aiogram logger namespaces.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Final

from loguru import logger

# Import your own project‑level settings
try:
    from src.constants import DEBUG, ENVIRONMENT  # type: ignore
except ImportError:  # Fallback defaults if constants are missing
    DEBUG: Final[bool] = bool(os.getenv("DEBUG", "0") == "1")
    ENVIRONMENT: Final[str] = os.getenv("ENVIRONMENT", "dev")  # "dev" | "prod"


class InterceptHandler(logging.Handler):
    """Redirect standard *logging* records to *loguru*.

    This handler is attached to the root logger **and** to individual
    libraries' loggers so that every record ends up in loguru with the
    correct caller depth and exception chain preserved.
    """

    def emit(self, record: logging.LogRecord) -> None:  # noqa: D401 (imperative mood)
        # Map logging levels between stdlib and loguru
        try:
            level = logger.level(record.levelname).name  # type: ignore[arg-type]
        except ValueError:
            level = record.levelno  # Fallback to numeric level if not found

        # Find the frame where the logging call was made, skipping internal frames
        frame = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """Configure *loguru* logging for an aiogram application.

    Example
    -------
    >>> from aiogram import Bot, Dispatcher, F
    >>>
    >>> setup_logging()
    >>> bot = Bot(token="…")
    >>> dp = Dispatcher()
    """

    # 1️⃣  Reset stdlib root logger and route everything through InterceptHandler
    logging.root.handlers = []
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

    aiogram_logger_names = (
        "aiogram",
        "aiogram.event",
        "aiogram.dispatcher",
        "aiogram.bot",
        "aiogram.client",
        "aiogram.session",
        "aiogram.webhook",
    )
    for name in aiogram_logger_names:
        _logger = logging.getLogger(name)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        _logger = logging.getLogger(name)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

    handlers: list[dict] = []

    if ENVIRONMENT.lower() == "prod":
        log_format = (
            "| <level>{level:<8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> – "
            "<level>{message}</level>"
        )
        handlers.append({
            "sink": sys.stderr,
            "format": log_format,
            "level": "INFO",
            "enqueue": True,
        })
    else:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> – "
            "<level>{message}</level>"
        )

        log_dir = os.getenv("LOG_DIR", "./log")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "bot.log")

        handlers.extend([
            {
                "sink": sys.stdout,
                "format": log_format,
                "level": "DEBUG" if DEBUG else "INFO",
                "enqueue": True,
            },
            {
                "sink": log_file_path,
                "rotation": "10 MB",
                "retention": "30 days",
                "compression": "zip",
                "enqueue": True,
                "level": "DEBUG" if DEBUG else "INFO",
                "format": log_format,
            },
        ])

    logger.configure(handlers=handlers)
    logger.success("Logging configured successfully for aiogram")


__all__ = ["setup_logging"]
