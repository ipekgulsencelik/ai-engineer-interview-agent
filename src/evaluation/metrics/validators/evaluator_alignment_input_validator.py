from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class EvaluatorAlignmentInputValidator:
    """
    Evaluator alignment input validation service.
    """

    @staticmethod
    def validate(
        *,
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
    ) -> None:
        if len(human_scores) != len(llm_scores):
            raise EvaluationValidationError(
                "human_scores and llm_scores must have the same length."
            )

        if len(human_labels) != len(llm_labels):
            raise EvaluationValidationError(
                "human_labels and llm_labels must have the same length."
            )

        if len(human_scores) != len(human_labels):
            raise EvaluationValidationError(
                "score and label sequences must have the same length."
            )