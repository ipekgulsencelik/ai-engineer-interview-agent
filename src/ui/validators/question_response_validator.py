from __future__ import annotations

from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)
from src.ui.schemas.question_response import (
    QuestionResponse,
)
from src.ui.schemas.question_response_schema import (
    QUESTION_RESPONSE_DIFFICULTY_RULE,
    QUESTION_RESPONSE_SCORE_RULE,
    QUESTION_RESPONSE_STRING_RULE,
)


class QuestionResponseValidator(
    BaseSchemaValidator,
):
    """
    QuestionResponse validation helper.
    """

    @classmethod
    def validate(
        cls,
        response: QuestionResponse,
    ) -> None:
        cls._validate_string(
            field_name="id",
            value=response.id,
        )

        cls._validate_string(
            field_name="text",
            value=response.text,
        )

        cls._validate_string(
            field_name="category",
            value=response.category,
        )

        cls._validate_string(
            field_name="level",
            value=response.level,
        )

        cls._validate_string(
            field_name="question_type",
            value=response.question_type,
        )

        cls._validate_difficulty(
            value=response.difficulty,
        )

        cls._validate_score(
            value=response.final_score,
        )

    @classmethod
    def _validate_string(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=QUESTION_RESPONSE_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=QUESTION_RESPONSE_STRING_RULE,
        )

    @classmethod
    def _validate_difficulty(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="difficulty",
            value=value,
            rules=QUESTION_RESPONSE_DIFFICULTY_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="difficulty",
            value=value,
            rules=QUESTION_RESPONSE_DIFFICULTY_RULE,
        )

    @classmethod
    def _validate_score(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="final_score",
            value=value,
            rules=QUESTION_RESPONSE_SCORE_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="final_score",
            value=value,
            rules=QUESTION_RESPONSE_SCORE_RULE,
        )