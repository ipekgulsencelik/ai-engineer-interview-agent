from __future__ import annotations

from src.application.normalizers.evaluation_metadata_normalizer import (
    EvaluationMetadataNormalizer,
)
from src.domain.constants.evaluation import (
    DEFAULT_CONFIDENCE_SCORE,
    DEFAULT_RUBRIC_VERSION,
)
from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)


class EvaluationMetadataFactory:
    """
    EvaluationMetadata value object üretir.

    Raw parser/provider output alır, normalize eder ve immutable domain model üretir.
    """

    @staticmethod
    def create(
        *,
        confidence: float = DEFAULT_CONFIDENCE_SCORE,
        rubric_version: str = DEFAULT_RUBRIC_VERSION,
        latency_seconds: float | None = None,
        missing_keywords: tuple[str, ...] | list[str] | None = None,
        follow_up_question: str | None = None,
    ) -> EvaluationMetadata:
        return EvaluationMetadata(
            confidence=confidence,
            rubric_version=(
                EvaluationMetadataNormalizer.normalize_optional_string(
                    rubric_version,
                )
                or DEFAULT_RUBRIC_VERSION
            ),
            latency_seconds=latency_seconds,
            missing_keywords=(
                EvaluationMetadataNormalizer.normalize_missing_keywords(
                    missing_keywords,
                )
            ),
            follow_up_question=(
                EvaluationMetadataNormalizer.normalize_optional_string(
                    follow_up_question,
                )
            ),
        )