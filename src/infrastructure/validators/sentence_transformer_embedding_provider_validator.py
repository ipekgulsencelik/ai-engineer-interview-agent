from __future__ import annotations

import math
from typing import Any

from src.infrastructure.errors.embedding_provider_error import (
    EmbeddingProviderError,
)
from src.infrastructure.schemas.sentence_transformer_embedding_provider_schema import (
    SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA,
)


class SentenceTransformerEmbeddingProviderValidator:
    """
    SentenceTransformer embedding provider validation helper.
    """

    @staticmethod
    def validate_model_name(
        model_name: str | None,
    ) -> None:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "model_name"
        ]

        if not isinstance(model_name, schema["type"]):
            raise EmbeddingProviderError(
                "model_name must be a string or None."
            )

        if (
            isinstance(model_name, str)
            and schema.get("non_empty", False)
            and not model_name.strip()
        ):
            raise EmbeddingProviderError(
                "model_name cannot be empty."
            )

    @staticmethod
    def validate_text(
        text: str,
    ) -> str:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "text"
        ]

        if not isinstance(text, schema["type"]):
            raise EmbeddingProviderError(
                "text must be a string."
            )

        normalized_text = text.strip()

        if schema.get("non_empty", False) and not normalized_text:
            raise EmbeddingProviderError(
                "text cannot be empty."
            )

        return normalized_text

    @classmethod
    def validate_texts(
        cls,
        texts: list[str],
    ) -> list[str]:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "texts"
        ]

        if not isinstance(texts, schema["type"]):
            raise EmbeddingProviderError(
                "texts must be a list."
            )

        if schema.get("allow_empty") is False and not texts:
            raise EmbeddingProviderError(
                "texts cannot be empty."
            )

        normalized_items: list[str] = []

        for item in texts:
            if not isinstance(item, schema["item_type"]):
                raise EmbeddingProviderError(
                    "texts must contain only strings."
                )

            normalized_item = item.strip()

            if (
                schema.get("strip_items") is True
                and not normalized_item
            ):
                raise EmbeddingProviderError(
                    "texts cannot contain empty strings."
                )

            normalized_items.append(normalized_item)

        return normalized_items

    @staticmethod
    def validate_retry_count(
        retry_count: int,
    ) -> None:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "retry_count"
        ]

        SentenceTransformerEmbeddingProviderValidator._validate_numeric_rule(
            field_name="retry_count",
            value=retry_count,
            schema=schema,
        )

    @staticmethod
    def validate_retry_backoff_seconds(
        retry_backoff_seconds: float,
    ) -> None:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "retry_backoff_seconds"
        ]

        SentenceTransformerEmbeddingProviderValidator._validate_numeric_rule(
            field_name="retry_backoff_seconds",
            value=retry_backoff_seconds,
            schema=schema,
        )

    @staticmethod
    def validate_batch_size(
        batch_size: int,
    ) -> None:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "batch_size"
        ]

        SentenceTransformerEmbeddingProviderValidator._validate_numeric_rule(
            field_name="batch_size",
            value=batch_size,
            schema=schema,
        )

    @staticmethod
    def validate_normalize_embeddings(
        normalize_embeddings: bool,
    ) -> None:
        schema = SENTENCE_TRANSFORMER_EMBEDDING_PROVIDER_SCHEMA[
            "normalize_embeddings"
        ]

        if not isinstance(normalize_embeddings, schema["type"]):
            raise EmbeddingProviderError(
                "normalize_embeddings must be a boolean."
            )

    @staticmethod
    def _validate_numeric_rule(
        *,
        field_name: str,
        value: Any,
        schema: dict[str, Any],
    ) -> None:
        expected_type = schema["type"]

        if (
            schema.get("allow_bool") is False
            and isinstance(value, bool)
        ):
            raise EmbeddingProviderError(
                f"{field_name} must not be a boolean."
            )

        if not isinstance(value, expected_type):
            raise EmbeddingProviderError(
                f"{field_name} has invalid type."
            )

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise EmbeddingProviderError(
                f"{field_name} must be finite."
            )

        min_value = schema.get("min_value")

        if min_value is not None and numeric_value < float(min_value):
            raise EmbeddingProviderError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )