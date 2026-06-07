from __future__ import annotations

from typing import TYPE_CHECKING

from src.infrastructure.schemas.benchmark_case_schema import (
    BENCHMARK_CASE_STRING_RULE,
)
from src.domain.validators.base_schema_validator import (
    BaseSchemaValidator,
)

if TYPE_CHECKING:
    from src.infrastructure.models.benchmark_case import (
        BenchmarkCase,
    )


class BenchmarkCaseValidator(
    BaseSchemaValidator,
):
    """
    BenchmarkCase validation helper.
    """

    @classmethod
    def validate(
        cls,
        benchmark_case: BenchmarkCase,
    ) -> None:
        cls._validate_string(
            field_name="query",
            value=benchmark_case.query,
        )

        cls._validate_string(
            field_name="expected_category",
            value=benchmark_case.expected_category,
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
            rules=BENCHMARK_CASE_STRING_RULE,
        )

        cls.validate_non_empty_string(
            field_name=field_name,
            value=value,
            rules=BENCHMARK_CASE_STRING_RULE,
        )