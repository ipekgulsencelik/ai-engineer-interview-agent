from __future__ import annotations

from src.ui.constants.evaluation_metric_labels import (
    COMMUNICATION_SCORE_LABEL,
    DEPTH_SCORE_LABEL,
    OVERALL_SCORE_LABEL,
    TECHNICAL_SCORE_LABEL,
)
from src.ui.presentation.evaluation_metric_item import (
    EvaluationMetricItem,
)
from src.ui.schemas.evaluation_response import (
    EvaluationResponse,
)


class EvaluationResponseFormatter:
    """
    UI formatting utilities for EvaluationResponse.
    """

    @staticmethod
    def format_score(
        *,
        score: float,
    ) -> str:
        return f"{score:.1f}"

    @staticmethod
    def to_metric_items(
        *,
        evaluation: EvaluationResponse,
    ) -> list[EvaluationMetricItem]:
        return [
            EvaluationResponseFormatter._build_metric_item(
                label=OVERALL_SCORE_LABEL,
                score=evaluation.score,
            ),
            EvaluationResponseFormatter._build_metric_item(
                label=TECHNICAL_SCORE_LABEL,
                score=evaluation.technical_accuracy,
            ),
            EvaluationResponseFormatter._build_metric_item(
                label=DEPTH_SCORE_LABEL,
                score=evaluation.depth,
            ),
            EvaluationResponseFormatter._build_metric_item(
                label=COMMUNICATION_SCORE_LABEL,
                score=evaluation.communication,
            ),
        ]

    @staticmethod
    def _build_metric_item(
        *,
        label: str,
        score: float,
    ) -> EvaluationMetricItem:
        return EvaluationMetricItem(
            label=label,
            value=EvaluationResponseFormatter.format_score(
                score=score,
            ),
        )