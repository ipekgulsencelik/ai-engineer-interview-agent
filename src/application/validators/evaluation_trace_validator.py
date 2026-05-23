from __future__ import annotations

from src.domain.schemas.evaluation_trace_schema import (
    EVALUATION_TRACE_SCORE_RULE,
    NON_EMPTY_EVALUATION_TRACE_STRING_RULE,
    NON_NEGATIVE_EVALUATION_LATENCY_RULE,
    NON_NEGATIVE_TOKENS_USED_RULE,
)
from src.domain.telemetry.evaluation_trace import (
    EvaluationTrace,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class EvaluationTraceValidator(
    BaseSchemaValidator,
):
    """
    EvaluationTrace validation helper.
    """

    @classmethod
    def validate(
        cls,
        trace: EvaluationTrace,
    ) -> None:
        cls._validate_non_empty_string(
            field_name="question_id",
            value=trace.question_id,
        )

        cls._validate_non_empty_string(
            field_name="model_name",
            value=trace.model_name,
        )

        cls._validate_tokens_used(
            value=trace.tokens_used,
        )

        cls._validate_latency_seconds(
            value=trace.latency_seconds,
        )

        cls._validate_score(
            value=trace.score,
        )

    @classmethod
    def _validate_non_empty_string(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=NON_EMPTY_EVALUATION_TRACE_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=NON_EMPTY_EVALUATION_TRACE_STRING_RULE,
        )

    @classmethod
    def _validate_tokens_used(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="tokens_used",
            value=value,
            rules=NON_NEGATIVE_TOKENS_USED_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="tokens_used",
            value=value,
            rules=NON_NEGATIVE_TOKENS_USED_RULE,
        )

    @classmethod
    def _validate_latency_seconds(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="latency_seconds",
            value=value,
            rules=NON_NEGATIVE_EVALUATION_LATENCY_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="latency_seconds",
            value=value,
            rules=NON_NEGATIVE_EVALUATION_LATENCY_RULE,
        )

    @classmethod
    def _validate_score(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="score",
            value=value,
            rules=EVALUATION_TRACE_SCORE_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="score",
            value=value,
            rules=EVALUATION_TRACE_SCORE_RULE,
        )