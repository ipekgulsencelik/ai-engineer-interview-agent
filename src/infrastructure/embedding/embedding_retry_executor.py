from __future__ import annotations

import logging
import time
from typing import Any

from src.infrastructure.errors.embedding_retry_error import (
    EmbeddingRetryError,
)

logger = logging.getLogger(__name__)


class EmbeddingRetryExecutor:
    """
    Embedding encode retry policy executor.
    """

    def __init__(
        self,
        *,
        retry_count: int,
        retry_backoff_seconds: float,
    ) -> None:
        self._retry_count = retry_count
        self._retry_backoff_seconds = retry_backoff_seconds

    def execute(
        self,
        *,
        model: Any,
        payload: str | list[str],
        normalize_embeddings: bool,
        batch_size: int,
    ) -> Any:
        last_error: Exception | None = None

        for attempt in range(1, self._retry_count + 2):
            try:
                return model.encode(
                    payload,
                    normalize_embeddings=normalize_embeddings,
                    batch_size=batch_size,
                    show_progress_bar=False,
                )

            except Exception as exc:
                last_error = exc

                logger.warning(
                    "Embedding encode failed "
                    "(attempt %s/%s): %s",
                    attempt,
                    self._retry_count + 1,
                    exc,
                )

                if attempt <= self._retry_count:
                    time.sleep(
                        self._retry_backoff_seconds * attempt
                    )

        raise EmbeddingRetryError(
            "Failed to generate embeddings after retries."
        ) from last_error