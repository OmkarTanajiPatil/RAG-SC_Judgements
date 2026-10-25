"""Application logging configuration.

The logger is configured lazily so importing project modules does not create
files or modify the root logger. Use :func:`get_logger` from application code.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

__all__ = ["configure_logging", "get_logger"]

_LOGGER_NAME = "rag_sc_judgements"
_DEFAULT_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_MAX_BYTES = 5 * 1024 * 1024
_BACKUP_COUNT = 3


def _resolve_level() -> int:
    """Return the configured log level, defaulting to ``INFO``."""

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, None)
    if not isinstance(level, int):
        raise TypeError(
            f"LOG_LEVEL must be a valid logging level, got {level_name!r}"
        )
    return level


def configure_logging() -> logging.Logger:
    """Configure and return the application's base logger.

    Configuration is idempotent: repeated calls reuse the existing handlers
    rather than duplicating log records.
    """

    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(_resolve_level())
    logger.propagate = False

    if logger.handlers:
        return logger

    log_dir = Path(os.getenv("LOG_DIR", str(_DEFAULT_LOG_DIR)))
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT)
    file_handler = RotatingFileHandler(
        log_dir / "application.log",
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if os.getenv("LOG_CONSOLE", "true").lower() in {"1", "true", "yes"}:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a configured child logger for ``name``."""

    base_logger = configure_logging()
    return base_logger if not name else base_logger.getChild(name)