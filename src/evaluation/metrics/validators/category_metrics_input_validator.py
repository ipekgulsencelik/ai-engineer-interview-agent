from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class CategoryMetricsInputValidator:
    """
    Category metrics analyzer input validation service.
    """

    @staticmethod
    def validate(
        *,
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
        categories: Sequence[str],
    ) -> None:
        CategoryMetricsInputValidator._validate_not_empty(
            categories=categories,
        )

        CategoryMetricsInputValidator._validate_lengths(
            expected_length=len(categories),
            human_scores=human_scores,
            llm_scores=llm_scores,
            human_labels=human_labels,
            llm_labels=llm_labels,
        )

        CategoryMetricsInputValidator._validate_categories(
            categories=categories,
        )

    @staticmethod
    def _validate_not_empty(
        *,
        categories: Sequence[str],
    ) -> None:
        if not categories:
            raise EvaluationValidationError(
                "categories cannot be empty."
            )

    @staticmethod
    def _validate_lengths(
        *,
        expected_length: int,
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
    ) -> None:
        if len(human_scores) != expected_length:
            raise EvaluationValidationError(
                "human_scores and categories must have the same length."
            )

        if len(llm_scores) != expected_length:
            raise EvaluationValidationError(
                "llm_scores and categories must have the same length."
            )

        if len(human_labels) != expected_length:
            raise EvaluationValidationError(
                "human_labels and categories must have the same length."
            )

        if len(llm_labels) != expected_length:
            raise EvaluationValidationError(
                "llm_labels and categories must have the same length."
            )

    @staticmethod
    def _validate_categories(
        *,
        categories: Sequence[str],
    ) -> None:
        for index, category in enumerate(categories):
            if not isinstance(category, str):
                raise EvaluationValidationError(
                    f"categories[{index}] must be a string."
                )

            if not category.strip():
                raise EvaluationValidationError(
                    f"categories[{index}] cannot be empty."
                )