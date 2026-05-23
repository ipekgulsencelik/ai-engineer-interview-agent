from __future__ import annotations

from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)
from src.infrastructure.models.benchmark_summary import (
    BenchmarkSummary,
)


class BenchmarkSummaryCalculator:
    """
    Benchmark summary calculator.
    """

    @staticmethod
    def calculate(
        *,
        results: list[BenchmarkResult],
    ) -> BenchmarkSummary:
        if not results:
            return BenchmarkSummary(
                total=0.0,
                category_hit_rate=0.0,
                average_latency_seconds=0.0,
                average_top_score=0.0,
            )

        top_scores = [
            result.top_score
            for result in results
            if result.top_score is not None
        ]

        return BenchmarkSummary(
            total=float(len(results)),
            category_hit_rate=round(
                BenchmarkSummaryCalculator._hit_count(
                    results=results,
                )
                / len(results),
                4,
            ),
            average_latency_seconds=round(
                BenchmarkSummaryCalculator._average_latency(
                    results=results,
                ),
                4,
            ),
            average_top_score=round(
                sum(top_scores) / len(top_scores),
                4,
            )
            if top_scores
            else 0.0,
        )

    @staticmethod
    def _hit_count(
        *,
        results: list[BenchmarkResult],
    ) -> int:
        return sum(
            1
            for result in results
            if result.category_hit
        )

    @staticmethod
    def _average_latency(
        *,
        results: list[BenchmarkResult],
    ) -> float:
        return (
            sum(
                result.latency_seconds
                for result in results
            )
            / len(results)
        )