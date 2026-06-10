from __future__ import annotations

from dataclasses import dataclass

from src.application.benchmarking.validators.benchmark_result_validator import (
    BenchmarkResultValidator,
)


@dataclass(frozen=True)
class BenchmarkResult:
    """
    Retrieval benchmark result snapshot.
    """

    query: str

    expected_category: str

    retrieved_count: int

    top_question_id: str | None

    top_score: float | None

    category_hit: bool

    latency_seconds: float

    def __post_init__(
        self,
    ) -> None:
        BenchmarkResultValidator.validate(
            self,
        )