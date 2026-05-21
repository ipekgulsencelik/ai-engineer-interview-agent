from __future__ import annotations


class SentenceTransformerModelLoadError(RuntimeError):
    """
    Raised when the SentenceTransformer model
    cannot be loaded.
    """