from __future__ import annotations

from dataclasses import dataclass

from src.infrastructure.validators.benchmark_case_validator import (
    BenchmarkCaseValidator,
)


@dataclass(frozen=True)
class BenchmarkCase:
    """
    Retrieval benchmark test case.
    """

    query: str

    expected_category: str

    def __post_init__(
        self,
    ) -> None:
        BenchmarkCaseValidator.validate(
            self,
        )