from __future__ import annotations

from src.application.constants.evaluation import (
    DEFAULT_CONFIDENCE_SCORE,
    DEFAULT_EVALUATION_SCORE,
    DEFAULT_FEEDBACK,
    DEFAULT_RUBRIC_VERSION,
    MAX_CONFIDENCE_SCORE,
    MAX_EVALUATION_SCORE,
    MIN_CONFIDENCE_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.application.models.evaluation_metadata import EvaluationMetadata
from src.application.models.evaluation_payload import EvaluationPayload
from src.domain.results.evaluation_result import EvaluationResult


class EvaluationResultFactory:
    """
    EvaluationPayload modelinden domain-safe EvaluationResult üretir.

    Business fallback ve clamping kararları burada tutulur.
    Mapper bu kuralları bilmez.
    """

    @classmethod
    def create(
        cls,
        *,
        payload: EvaluationPayload,
        metadata: EvaluationMetadata | None = None,
    ) -> EvaluationResult:
        return EvaluationResult(
            score=cls._score_or_default(payload.score),
            feedback=cls._string_or_default(
                value=payload.feedback,
                fallback=DEFAULT_FEEDBACK,
            ),
            technical_accuracy=cls._score_or_default(
                payload.technical_accuracy
            ),
            depth=cls._score_or_default(payload.depth),
            communication=cls._score_or_default(payload.communication),
            missing_keywords=payload.missing_keywords,
            follow_up_question=payload.follow_up_question,
            confidence=cls._confidence_or_default(payload.confidence),
            rubric_version=cls._string_or_default(
                value=payload.rubric_version,
                fallback=DEFAULT_RUBRIC_VERSION,
            ),
            metadata=metadata or EvaluationMetadata(),
        )

    @staticmethod
    def _score_or_default(
        value: float | None,
    ) -> float:
        if value is None:
            return DEFAULT_EVALUATION_SCORE

        return max(
            MIN_EVALUATION_SCORE,
            min(MAX_EVALUATION_SCORE, value),
        )

    @staticmethod
    def _confidence_or_default(
        value: float | None,
    ) -> float:
        if value is None:
            return DEFAULT_CONFIDENCE_SCORE

        return max(
            MIN_CONFIDENCE_SCORE,
            min(MAX_CONFIDENCE_SCORE, value),
        )

    @staticmethod
    def _string_or_default(
        *,
        value: str | None,
        fallback: str,
    ) -> str:
        if value is None:
            return fallback

        normalized_value = value.strip()

        if not normalized_value:
            return fallback

        return normalized_value