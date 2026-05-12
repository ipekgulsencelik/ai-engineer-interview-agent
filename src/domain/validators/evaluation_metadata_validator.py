from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.metadata.evaluation_metadata import (
        EvaluationMetadata,
    )


class EvaluationMetadataValidator:
    """
    EvaluationMetadata invariant validation rules.
    """

    @classmethod
    def validate(
        cls,
        metadata: EvaluationMetadata,
    ) -> None:
        cls._validate_confidence(
            metadata.confidence,
        )
        cls._validate_rubric_version(
            metadata.rubric_version,
        )
        cls._validate_latency_seconds(
            metadata.latency_seconds,
        )
        cls._validate_missing_keywords(
            metadata.missing_keywords,
        )
        cls._validate_follow_up_question(
            metadata.follow_up_question,
        )

    @staticmethod
    def _validate_confidence(
        value: float,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(
                "confidence must be numeric."
            )

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValueError(
                "confidence must be finite."
            )

        if not 0.0 <= numeric_value <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0."
            )

    @staticmethod
    def _validate_rubric_version(
        value: str,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "rubric_version must be a string."
            )

        if not value.strip():
            raise ValueError(
                "rubric_version cannot be empty."
            )

    @staticmethod
    def _validate_latency_seconds(
        value: float | None,
    ) -> None:
        if value is None:
            return

        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(
                "latency_seconds must be numeric."
            )

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValueError(
                "latency_seconds must be finite."
            )

        if numeric_value < 0.0:
            raise ValueError(
                "latency_seconds cannot be negative."
            )

    @staticmethod
    def _validate_missing_keywords(
        value: tuple[str, ...],
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(
                "missing_keywords must be a tuple."
            )

        for keyword in value:
            if not isinstance(keyword, str):
                raise TypeError(
                    "missing_keywords items must be strings."
                )

            if not keyword.strip():
                raise ValueError(
                    "missing_keywords items cannot be empty."
                )

    @staticmethod
    def _validate_follow_up_question(
        value: str | None,
    ) -> None:
        if value is None:
            return

        if not isinstance(value, str):
            raise TypeError(
                "follow_up_question must be a string."
            )

        if not value.strip():
            raise ValueError(
                "follow_up_question cannot be empty."
            )