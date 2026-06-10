from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.agreements import (
    MIN_AGREEMENT_SAMPLE_COUNT,
)


class AgreementInputValidator:
    """
    Agreement input validation service.
    """

    @staticmethod
    def validate(
        *,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
    ) -> None:
        if len(evaluator_a_labels) != len(evaluator_b_labels):
            raise EvaluationValidationError(
                "evaluator label sequences must have the same length."
            )

        if len(evaluator_a_labels) < MIN_AGREEMENT_SAMPLE_COUNT:
            raise EvaluationValidationError(
                "evaluator label sequences cannot be empty."
            )

        AgreementInputValidator._validate_label_series(
            field_name="evaluator_a_labels",
            labels=evaluator_a_labels,
        )

        AgreementInputValidator._validate_label_series(
            field_name="evaluator_b_labels",
            labels=evaluator_b_labels,
        )

    @staticmethod
    def _validate_label_series(
        *,
        field_name: str,
        labels: Sequence[str],
    ) -> None:
        for index, label in enumerate(labels):
            if not isinstance(
                label,
                str,
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be a string."
                )

            if not label.strip():
                raise EvaluationValidationError(
                    f"{field_name}[{index}] cannot be empty."
                )