from __future__ import annotations

from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)


class InterviewStepRequestValidator:
    """
    InterviewStepRequest schema normalization helper.
    """

    @staticmethod
    def normalize_current_level(
        value: object,
    ) -> object:
        if isinstance(value, QuestionLevel):
            return value

        if not isinstance(value, str):
            return value

        normalized_value = (
            value.strip()
            .upper()
        )

        if not normalized_value:
            return value

        return normalized_value