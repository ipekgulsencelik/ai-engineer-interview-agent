"""Fail-closed runtime policy for unpatched legacy ChromaDB integration."""

from __future__ import annotations

from src.config.settings import settings
from src.infrastructure.errors.vector_store_error import VectorStoreError


class LegacyChromaPolicy:
    @staticmethod
    def require_safe_environment() -> None:
        if (
            not settings.LEGACY_CHROMA_ENABLED
            or settings.ENV.strip().lower() not in {"development", "test"}
        ):
            raise VectorStoreError(
                "Legacy ChromaDB is disabled outside isolated development/test. "
                "Use the embedded SQLite question store."
            )
