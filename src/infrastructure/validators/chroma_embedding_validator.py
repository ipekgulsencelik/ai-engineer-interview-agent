
from __future__ import annotations

import math
from collections.abc import Sequence


class ChromaEmbeddingValidator:
    """Validation rules for Chroma embedding inputs."""

    @classmethod
    def validate_embedding(
        cls,
        embedding: Sequence[float],
        *,
        field_name: str = "embedding",
    ) -> None:

        if isinstance(embedding, (str, bytes)):
            raise TypeError(f"{field_name} must be a sequence of numbers.")

        if not isinstance(embedding, Sequence):
            raise TypeError(f"{field_name} must be a sequence of numbers.")

        if len(embedding) == 0:
            raise ValueError(f"{field_name} cannot be empty.")

        for index, value in enumerate(embedding):
            cls._validate_numeric_value(
                value=value,
                field_name=field_name,
                index=index,
            )

    @classmethod
    def validate_embeddings(
        cls,
        embeddings: Sequence[Sequence[float]],
        *,
        expected_count: int | None = None,
        field_name: str = "embeddings",
    ) -> None:
        if isinstance(embeddings, (str, bytes)):
            raise TypeError(f"{field_name} must be a sequence of embeddings.")

        if not isinstance(embeddings, Sequence):
            raise TypeError(f"{field_name} must be a sequence of embeddings.")

        if len(embeddings) == 0:
            raise ValueError(f"{field_name} cannot be empty.")

        if expected_count is not None and len(embeddings) != expected_count:
            raise ValueError(
                f"{field_name} count must match expected_count. "
                f"Expected {expected_count}, got {len(embeddings)}."
            )

        first_dimension = len(embeddings[0])

        for index, embedding in enumerate(embeddings):
            cls.validate_embedding(
                embedding=embedding,
                field_name=f"{field_name}[{index}]",
            )

            if len(embedding) != first_dimension:
                raise ValueError(
                    f"All embeddings must have the same dimension. "
                    f"Expected {first_dimension}, got {len(embedding)} "
                    f"at index {index}."
                )

    @staticmethod
    def _validate_numeric_value(
        value: object,
        field_name: str,
        index: int,
    ) -> None:

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"{field_name} must contain only numeric values. "
                f"Invalid value at index {index}: {value!r}."
            )

        numeric_value = float(value)

        if math.isnan(numeric_value):
            raise ValueError(
                f"{field_name} cannot contain NaN values. "
                f"Invalid value at index {index}."
            )

        if math.isinf(numeric_value):
            raise ValueError(
                f"{field_name} cannot contain infinite values. "
                f"Invalid value at index {index}."
            )