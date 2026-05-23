from __future__ import annotations

from src.infrastructure.models.benchmark_case import (
    BenchmarkCase,
)
from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)


class BenchmarkResultFactory:
    """
    BenchmarkResult factory.
    """

    @staticmethod
    def create(
        *,
        benchmark_case: BenchmarkCase,
        retrieved_count: int,
        top_question_id: str | None,
        top_score: float | None,
        category_hit: bool,
        latency_seconds: float,
    ) -> BenchmarkResult:
        return BenchmarkResult(
            query=benchmark_case.query,
            expected_category=benchmark_case.expected_category,
            retrieved_count=retrieved_count,
            top_question_id=top_question_id,
            top_score=top_score,
            category_hit=category_hit,
            latency_seconds=latency_seconds,
        )