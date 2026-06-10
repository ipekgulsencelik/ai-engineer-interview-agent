from __future__ import annotations

from src.api.schemas.evaluation.responses import (
    EvaluationResponse,
)
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class EvaluationResponseMapper:
    """
    EvaluationResult -> EvaluationResponse mapper.
    """

    @staticmethod
    def from_result(
        *,
        result: EvaluationResult,
    ) -> EvaluationResponse:
        return EvaluationResponse(
            score=result.score,
            feedback=result.feedback,
            technical_accuracy=(
                result.technical_accuracy
            ),
            depth=result.depth,
            communication=(
                result.communication
            ),
            confidence=(
                result.metadata.confidence
            ),
            missing_keywords=list(
                result.metadata.missing_keywords,
            ),
            follow_up_question=(
                result.metadata.follow_up_question
            ),
            latency_seconds=(
                result.metadata.latency_seconds
            ),
        )