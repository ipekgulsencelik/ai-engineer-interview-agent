from __future__ import annotations

from src.infrastructure.errors.question_lookup_error import (
    QuestionLookupError,
)
from src.infrastructure.schemas.question_lookup_schema import (
    QUESTION_LOOKUP_SCHEMA,
)


class QuestionLookupValidator:
    """
    Question lookup validation helper.
    """

    @staticmethod
    def validate_question_id(
        question_id: str,
    ) -> None:
        schema = QUESTION_LOOKUP_SCHEMA[
            "question_id"
        ]

        if not isinstance(question_id, schema["type"]):
            raise QuestionLookupError(
                "question_id must be a string."
            )

        normalized = question_id.strip()

        if schema.get("non_empty", False) and not normalized:
            raise QuestionLookupError(
                "question_id cannot be empty."
            )

        if schema.get("strip", False) and question_id != normalized:
            raise QuestionLookupError(
                "question_id cannot have leading or trailing whitespace."
            )

        if len(normalized) > 255:
            raise QuestionLookupError(
                "question_id cannot exceed 255 characters."
            )

        if " " in normalized:
            raise QuestionLookupError(
                "question_id cannot contain spaces."
            )

        if not all(c.isalnum() or c in ("-", "_") for c in normalized):
            raise QuestionLookupError(
                "question_id can only contain alphanumeric characters, "
                "hyphens, or underscores."
            )