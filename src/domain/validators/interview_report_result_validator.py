from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.results.interview_report_result import InterviewReportResult


class InterviewReportResultValidator:
    """
    Validation helper for final interview report snapshots.
    """

    @classmethod
    def validate(
        cls,
        result: "InterviewReportResult",
    ) -> None:
        cls._validate_non_empty_string(
            field_name="candidate_level",
            value=result.candidate_level,
        )
        cls._validate_score(
            field_name="overall_score",
            value=result.overall_score,
        )
        cls._validate_score(
            field_name="market_alignment_score",
            value=result.market_alignment_score,
        )
        cls._validate_non_negative_int(
            field_name="evaluated_questions",
            value=result.evaluated_questions,
        )
        cls._validate_string_tuple(
            field_name="strengths",
            value=result.strengths,
        )
        cls._validate_string_tuple(
            field_name="weaknesses",
            value=result.weaknesses,
        )
        cls._validate_string_tuple(
            field_name="recommendations",
            value=result.recommendations,
        )
        cls._validate_category_scores(
            value=result.category_scores,
        )

    @classmethod
    def _validate_non_empty_string(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")

        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    @classmethod
    def _validate_score(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{field_name} must be numeric.")

        if not math.isfinite(float(value)):
            raise ValueError(f"{field_name} must be finite.")

    @classmethod
    def _validate_non_negative_int(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field_name} must be an integer.")

        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    @classmethod
    def _validate_string_tuple(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(f"{field_name} must be a tuple.")

        for item in value:
            cls._validate_non_empty_string(
                field_name=f"{field_name} item",
                value=item,
            )

    @classmethod
    def _validate_category_scores(
        cls,
        *,
        value: object,
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError("category_scores must be a tuple.")

        for item in value:
            if not isinstance(item, tuple) or len(item) != 2:
                raise TypeError(
                    "category_scores items must be (category, score) tuples."
                )

            category, score = item
            cls._validate_non_empty_string(
                field_name="category_scores category",
                value=category,
            )
            cls._validate_score(
                field_name="category_scores score",
                value=score,
            )
