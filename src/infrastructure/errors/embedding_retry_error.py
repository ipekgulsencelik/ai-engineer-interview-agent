from __future__ import annotations


class EmbeddingRetryError(RuntimeError):
    """
    Raised when embedding generation fails after retry attempts.
    """