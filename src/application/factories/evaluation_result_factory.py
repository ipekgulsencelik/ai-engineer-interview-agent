from __future__ import annotations

from src.application.models.evaluation_payload import (
    EvaluationPayload,
)
from src.domain.constants.evaluation import (
    MAX_CONFIDENCE_SCORE,
    MAX_EVALUATION_SCORE,
    MIN_CONFIDENCE_SCORE,
    MIN_EVALUATION_SCORE,
    DEFAULT_COMMUNICATION_SCORE,
    DEFAULT_CONFIDENCE_SCORE,
    DEFAULT_DEPTH_SCORE,
    DEFAULT_EVALUATION_SCORE,
    DEFAULT_FEEDBACK,
    DEFAULT_RUBRIC_VERSION,
    DEFAULT_TECHNICAL_ACCURACY_SCORE,
)
from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


RUBRIC_TECHNICAL_WEIGHT = 0.40
RUBRIC_DEPTH_WEIGHT = 0.35
RUBRIC_COMMUNICATION_WEIGHT = 0.25


class EvaluationResultFactory:
    """
    EvaluationPayload modelinden domain-safe EvaluationResult üretir.
    """

    @classmethod
    def create(
        cls,
        payload: EvaluationPayload,
    ) -> EvaluationResult:
        cls._validate_payload(payload)

        metadata = EvaluationMetadata(
            confidence=cls._clamp(
                cls._number_or_default(
                    value=payload.confidence,
                    default=DEFAULT_CONFIDENCE_SCORE,
                ),
                low=MIN_CONFIDENCE_SCORE,
                high=MAX_CONFIDENCE_SCORE,
            ),
            rubric_version=cls._string_or_default(
                value=payload.rubric_version,
                default=DEFAULT_RUBRIC_VERSION,
            ),
            missing_keywords=tuple(
                keyword.strip()
                for keyword in payload.missing_keywords or ()
                if keyword and keyword.strip()
            ),
            follow_up_question=(
                payload.follow_up_question.strip()
                if payload.follow_up_question
                and payload.follow_up_question.strip()
                else None
            ),
        )

        return EvaluationResult(
            score=cls._overall_score(payload),
            feedback=cls._string_or_default(
                value=payload.feedback,
                default=DEFAULT_FEEDBACK,
            ),
            technical_accuracy=cls._score(payload.technical_accuracy, default=DEFAULT_TECHNICAL_ACCURACY_SCORE),
            depth=cls._score(payload.depth, default=DEFAULT_DEPTH_SCORE),
            communication=cls._score(payload.communication, default=DEFAULT_COMMUNICATION_SCORE),
            metadata=metadata,
        )

    @classmethod
    def _overall_score(
        cls,
        payload: EvaluationPayload,
    ) -> float:
        """Weighted rubric score (DECISIONS.md decision 9) when all
        dimensions are present; otherwise the evaluator's own score."""
        dimensions = (
            payload.technical_accuracy,
            payload.depth,
            payload.communication,
        )
        if all(value is not None for value in dimensions):
            technical, depth, communication = (
                cls._score(value, default=0.0) for value in dimensions
            )
            return round(
                RUBRIC_TECHNICAL_WEIGHT * technical
                + RUBRIC_DEPTH_WEIGHT * depth
                + RUBRIC_COMMUNICATION_WEIGHT * communication,
                1,
            )
        return cls._score(payload.score, default=DEFAULT_EVALUATION_SCORE)

    @classmethod
    def _score(
        cls,
        value: float | None,
        *,
        default: float,
    ) -> float:
        return cls._clamp(
            cls._number_or_default(value=value, default=default),
            low=MIN_EVALUATION_SCORE,
            high=MAX_EVALUATION_SCORE,
        )

    @staticmethod
    def _clamp(
        value: float,
        *,
        low: float,
        high: float,
    ) -> float:
        return min(max(value, low), high)

    @staticmethod
    def _validate_payload(
        payload: EvaluationPayload,
    ) -> None:
        if not isinstance(payload, EvaluationPayload):
            raise TypeError(
                "payload must be an EvaluationPayload."
            )

    @staticmethod
    def _number_or_default(
        *,
        value: float | None,
        default: float,
    ) -> float:
        if value is None:
            return default

        return float(value)

    @staticmethod
    def _string_or_default(
        *,
        value: str | None,
        default: str,
    ) -> str:
        if value is None:
            return default

        normalized = value.strip()

        if not normalized:
            return default

        return normalized