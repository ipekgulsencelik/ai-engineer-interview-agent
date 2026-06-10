from __future__ import annotations

from typing import Any

from src.application.errors.question_rehydration_error import (
    QuestionRehydrationError,
)


class QuestionRehydrationInputValidator:
    """
    Question rehydration input validation helper.
    """

    @staticmethod
    def validate_question_id(
        *,
        question_id: str,
    ) -> None:
        if not isinstance(question_id, str):
            raise QuestionRehydrationError(
                "question_id must be a string."
            )

        if not question_id.strip():
            raise QuestionRehydrationError(
                "question_id cannot be empty."
            )

    @staticmethod
    def validate_metadata(
        *,
        metadata: dict[str, Any],
    ) -> None:
        if not isinstance(metadata, dict):
            raise QuestionRehydrationError(
                "metadata must be a dictionary."
            )