from __future__ import annotations

from src.application.models.evaluation_payload import (
    EvaluationPayload,
)
from src.domain.constants.evaluation import (
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
            confidence=cls._number_or_default(
                value=payload.confidence,
                default=DEFAULT_CONFIDENCE_SCORE,
            ),
            rubric_version=cls._string_or_default(
                value=payload.rubric_version,
                default=DEFAULT_RUBRIC_VERSION,
            ),
        )

        return EvaluationResult(
            score=cls._number_or_default(
                value=payload.score,
                default=DEFAULT_EVALUATION_SCORE,
            ),
            feedback=cls._string_or_default(
                value=payload.feedback,
                default=DEFAULT_FEEDBACK,
            ),
            technical_accuracy=cls._number_or_default(
                value=payload.technical_accuracy,
                default=DEFAULT_TECHNICAL_ACCURACY_SCORE,
            ),
            depth=cls._number_or_default(
                value=payload.depth,
                default=DEFAULT_DEPTH_SCORE,
            ),
            communication=cls._number_or_default(
                value=payload.communication,
                default=DEFAULT_COMMUNICATION_SCORE,
            ),
            missing_keywords=payload.missing_keywords
            or tuple(),
            follow_up_question=payload.follow_up_question,
            metadata=metadata,
        )

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