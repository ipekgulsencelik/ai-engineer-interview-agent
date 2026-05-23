from __future__ import annotations

from typing import TYPE_CHECKING

from src.infrastructure.validations.benchmark_result_schema import (
    BENCHMARK_RESULT_BOOLEAN_RULE,
    BENCHMARK_RESULT_LATENCY_RULE,
    BENCHMARK_RESULT_OPTIONAL_SCORE_RULE,
    BENCHMARK_RESULT_OPTIONAL_STRING_RULE,
    BENCHMARK_RESULT_RETRIEVED_COUNT_RULE,
    BENCHMARK_RESULT_STRING_RULE,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)

if TYPE_CHECKING:
    from src.infrastructure.models.benchmark_result import (
        BenchmarkResult,
    )


class BenchmarkResultValidator(
    BaseSchemaValidator,
):
    """
    BenchmarkResult validation helper.
    """

    @classmethod
    def validate(
        cls,
        result: BenchmarkResult,
    ) -> None:
        cls._validate_string(
            field_name="query",
            value=result.query,
        )

        cls._validate_string(
            field_name="expected_category",
            value=result.expected_category,
        )

        cls._validate_retrieved_count(
            value=result.retrieved_count,
        )

        cls._validate_optional_string(
            field_name="top_question_id",
            value=result.top_question_id,
        )

        cls._validate_optional_score(
            field_name="top_score",
            value=result.top_score,
        )

        cls._validate_boolean(
            field_name="category_hit",
            value=result.category_hit,
        )

        cls._validate_latency(
            value=result.latency_seconds,
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
            rules=BENCHMARK_RESULT_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=BENCHMARK_RESULT_STRING_RULE,
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
            rules=BENCHMARK_RESULT_OPTIONAL_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=BENCHMARK_RESULT_OPTIONAL_STRING_RULE,
        )

    @classmethod
    def _validate_retrieved_count(
        cls,
        *,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name="retrieved_count",
            value=value,
            rules=BENCHMARK_RESULT_RETRIEVED_COUNT_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="retrieved_count",
            value=value,
            rules=BENCHMARK_RESULT_RETRIEVED_COUNT_RULE,
        )

    @classmethod
    def _validate_optional_score(
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
            rules=BENCHMARK_RESULT_OPTIONAL_SCORE_RULE,
        )

        cls.validate_numeric_bounds(
            field_name=field_name,
            value=value,
            rules=BENCHMARK_RESULT_OPTIONAL_SCORE_RULE,
        )

    @classmethod
    def _validate_boolean(
        cls,
        *,
        field_name: str,
        value: object,
    ) -> None:
        cls.validate_type(
            field_name=field_name,
            value=value,
            rules=BENCHMARK_RESULT_BOOLEAN_RULE,
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
            rules=BENCHMARK_RESULT_LATENCY_RULE,
        )

        cls.validate_numeric_bounds(
            field_name="latency_seconds",
            value=value,
            rules=BENCHMARK_RESULT_LATENCY_RULE,
        )