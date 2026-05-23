from __future__ import annotations

from src.domain.schemas.interview_trace_schema import (
    NON_EMPTY_TRACE_STRING_RULE,
    NON_NEGATIVE_INTEGER_RULE,
    NON_NEGATIVE_LATENCY_RULE,
)
from src.domain.telemetry.interview_trace import (
    InterviewTrace,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class InterviewTraceValidator(
    BaseSchemaValidator,
):
    """
    InterviewTrace validation helper.
    """

    @classmethod
    def validate(
        cls,
        trace: InterviewTrace,
    ) -> None:
        cls._validate_non_empty_trace_string(
            field_name="query",
            value=trace.query,
        )

        cls._validate_non_empty_trace_string(
            field_name="selected_question_id",
            value=trace.selected_question_id,
        )

        cls._validate_non_negative_integer(
            field_name="retrieved_candidates",
            value=trace.retrieved_candidates,
        )

        cls._validate_non_negative_latency(
            field_name="retrieval_latency_seconds",
            value=trace.retrieval_latency_seconds,
        )

        cls._validate_non_negative_latency(
            field_name="ranking_latency_seconds",
            value=trace.ranking_latency_seconds,
        )

        cls._validate_non_negative_latency(
            field_name="total_latency_seconds",
            value=trace.total_latency_seconds,
        )

    @classmethod
    def _validate_non_empty_trace_string(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=NON_EMPTY_TRACE_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=NON_EMPTY_TRACE_STRING_RULE,
        )

    @classmethod
    def _validate_non_negative_integer(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=NON_NEGATIVE_INTEGER_RULE,
        )

        cls.validate_numeric_bounds(
            field_name=field_name,
            value=value,
            rules=NON_NEGATIVE_INTEGER_RULE,
        )

    @classmethod
    def _validate_non_negative_latency(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=NON_NEGATIVE_LATENCY_RULE,
        )

        cls.validate_numeric_bounds(
            field_name=field_name,
            value=value,
            rules=NON_NEGATIVE_LATENCY_RULE,
        )