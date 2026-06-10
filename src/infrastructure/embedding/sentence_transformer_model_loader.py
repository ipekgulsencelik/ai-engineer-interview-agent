from __future__ import annotations

from typing import Any

from src.infrastructure.errors.sentence_transformer_model_load_error import (
    SentenceTransformerModelLoadError,
)


class SentenceTransformerModelLoader:
    """
    SentenceTransformer model loading adapter.
    """

    @staticmethod
    def load(
        *,
        model_name: str,
    ) -> Any:
        try:
            from sentence_transformers import SentenceTransformer

            return SentenceTransformer(model_name)

        except Exception as exc:
            raise SentenceTransformerModelLoadError(
                f"Failed to load embedding model: {model_name}"
            ) from exc