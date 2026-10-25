"""Qdrant connection helpers.

The default configuration targets the local Qdrant instance from
``docker-compose.yml``. Set ``QDRANT_URL`` (and optionally
``QDRANT_API_KEY`` and ``QDRANT_TIMEOUT``) when connecting to another
instance.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from qdrant_client import QdrantClient

from core.logger import get_logger

__all__ = ["QdrantSettings", "connect_to_qdrant", "create_qdrant_client"]

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class QdrantSettings:
    """Connection settings for a Qdrant server."""

    url: str = "http://127.0.0.1:6333"
    api_key: str | None = None
    timeout: float = 10.0

    @classmethod
    def from_environment(cls) -> QdrantSettings:
        """Build settings from environment variables.

        ``QDRANT_URL`` takes precedence over ``QDRANT_HOST`` and
        ``QDRANT_PORT``. The latter two are provided for deployments that
        configure the server as separate host/port values.
        """

        url = os.getenv("QDRANT_URL")
        if not url:
            host = os.getenv("QDRANT_HOST", "127.0.0.1")
            port = os.getenv("QDRANT_PORT", "6333")
            url = f"http://{host}:{port}"

        api_key = os.getenv("QDRANT_API_KEY") or None
        timeout_value = os.getenv("QDRANT_TIMEOUT", "10")
        try:
            timeout = float(timeout_value)
        except ValueError as error:
            raise ValueError("QDRANT_TIMEOUT must be a number of seconds") from error

        if timeout <= 0:
            raise ValueError("QDRANT_TIMEOUT must be greater than zero")

        return cls(url=url, api_key=api_key, timeout=timeout)


def create_qdrant_client(
    settings: QdrantSettings | None = None,
) -> QdrantClient:
    """Create a Qdrant client without making a network request."""

    resolved_settings = settings or QdrantSettings.from_environment()
    client_kwargs: dict[str, str | float] = {
        "url": resolved_settings.url,
        "timeout": resolved_settings.timeout,
    }
    if resolved_settings.api_key:
        client_kwargs["api_key"] = resolved_settings.api_key

    return QdrantClient(**client_kwargs)


def connect_to_qdrant(
    settings: QdrantSettings | None = None,
) -> QdrantClient:
    """Create a client and verify that the Qdrant server is reachable.

    Raises the original Qdrant or network exception when the server cannot
    be reached, so startup failures are visible to the caller.
    """

    resolved_settings = settings or QdrantSettings.from_environment()
    client = create_qdrant_client(resolved_settings)
    try:
        client.get_collections()
    except Exception:
        logger.exception("Unable to connect to Qdrant at %s", resolved_settings.url)
        raise
    logger.info("Connected to Qdrant at %s", resolved_settings.url)
    return client

if __name__ == "__main__":
    connect_to_qdrant()
    