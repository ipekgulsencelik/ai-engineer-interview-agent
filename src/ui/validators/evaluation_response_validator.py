from __future__ import annotations

from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)
from src.ui.schemas.evaluation_response import (
    EvaluationResponse,
)
from src.ui.schemas.evaluation_response_schema import (
    EVALUATION_RESPONSE_LATENCY_RULE,
    EVALUATION_RESPONSE_OPTIONAL_STRING_RULE,
    EVALUATION_RESPONSE_SCORE_RULE,
    EVALUATION_RESPONSE_STRING_RULE,
    EVALUATION_RESPONSE_STRING_TUPLE_RULE,
)


class EvaluationResponseValidator(
    BaseSchemaValidator,
):
    """
    EvaluationResponse validation helper.
    """

    @classmethod
    def validate(
        cls,
        response: EvaluationResponse,
    ) -> None:
        cls._validate_score(
            field_name="score",
            value=response.score,
        )

        cls._validate_score(
            field_name="technical_accuracy",
            value=response.technical_accuracy,
        )

        cls._validate_score(
            field_name="depth",
            value=response.depth,
        )

        cls._validate_score(
            field_name="communication",
            value=response.communication,
        )

        cls._validate_score(
            field_name="confidence",
            value=response.confidence,
        )

        cls._validate_string(
            field_name="feedback",
            value=response.feedback,
        )

        cls._validate_optional_string(
            field_name="follow_up_question",
            value=response.follow_up_question,
        )

        cls._validate_latency(
            value=response.latency_seconds,
        )

        cls._validate_string_tuple(
            value=response.missing_keywords,
        )

    @classmethod
    def _validate_score(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=EVALUATION_RESPONSE_SCORE_RULE,
        )

        cls.validate_numeric_bounds(
            field_name=field_name,
            value=value,
            rules=EVALUATION_RESPONSE_SCORE_RULE,
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
            rules=EVALUATION_RESPONSE_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=EVALUATION_RESPONSE_STRING_RULE,
        )

    @classmethod
    def _validate_optional_string(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        if value is None:
            return

        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=EVALUATION_RESPONSE_OPTIONAL_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=EVALUATION_RESPONSE_OPTIONAL_STRING_RULE,
        )

    @classmethod
    def _validate_latency(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="latency_seconds",
            value=value,
            rules=EVALUATION_RESPONSE_LATENCY_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="latency_seconds",
            value=value,
            rules=EVALUATION_RESPONSE_LATENCY_RULE,
        )

    @classmethod
    def _validate_string_tuple(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="missing_keywords",
            value=value,
            rules=EVALUATION_RESPONSE_STRING_TUPLE_RULE,
        )

        cls.validate_tuple_items(
            field_name="missing_keywords",
            value=value,
            rules=EVALUATION_RESPONSE_STRING_TUPLE_RULE,
        )