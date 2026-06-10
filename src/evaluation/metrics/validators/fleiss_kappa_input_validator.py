from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.agreements import (
    MIN_AGREEMENT_SAMPLE_COUNT,
    MIN_FLEISS_EVALUATOR_COUNT,
)


class FleissKappaInputValidator:
    """
    Fleiss kappa input validation service.
    """

    @staticmethod
    def validate(
        *,
        label_matrix: Sequence[Sequence[str]],
    ) -> None:
        if len(label_matrix) < MIN_AGREEMENT_SAMPLE_COUNT:
            raise EvaluationValidationError(
                "label_matrix cannot be empty."
            )

        evaluator_count = len(
            label_matrix[0],
        )

        if evaluator_count < MIN_FLEISS_EVALUATOR_COUNT:
            raise EvaluationValidationError(
                "Fleiss kappa requires at least "
                f"{MIN_FLEISS_EVALUATOR_COUNT} evaluators."
            )

        FleissKappaInputValidator._validate_rows(
            label_matrix=label_matrix,
            evaluator_count=evaluator_count,
        )

    @staticmethod
    def _validate_rows(
        *,
        label_matrix: Sequence[Sequence[str]],
        evaluator_count: int,
    ) -> None:
        for sample_index, labels in enumerate(label_matrix):
            if len(labels) != evaluator_count:
                raise EvaluationValidationError(
                    "all label_matrix rows must have the same evaluator count."
                )

            FleissKappaInputValidator._validate_labels(
                labels=labels,
                sample_index=sample_index,
            )

    @staticmethod
    def _validate_labels(
        *,
        labels: Sequence[str],
        sample_index: int,
    ) -> None:
        for label_index, label in enumerate(labels):
            if not isinstance(label, str):
                raise EvaluationValidationError(
                    "label_matrix"
                    f"[{sample_index}]"
                    f"[{label_index}] must be a string."
                )

            if not label.strip():
                raise EvaluationValidationError(
                    "label_matrix"
                    f"[{sample_index}]"
                    f"[{label_index}] cannot be empty."
                )