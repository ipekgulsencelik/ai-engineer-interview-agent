from __future__ import annotations

from src.evaluation.metrics.constants.benchmark import (
    MODERATE_BENCHMARK_INTERPRETATION,
    MODERATE_BENCHMARK_THRESHOLD,
    STRONG_BENCHMARK_INTERPRETATION,
    STRONG_BENCHMARK_THRESHOLD,
    WEAK_BENCHMARK_INTERPRETATION,
)


class BenchmarkInterpreter:
    """
    Benchmark quality interpretation service.
    """

    @staticmethod
    def interpret(
        *,
        benchmark_score: float,
    ) -> str:
        if benchmark_score >= STRONG_BENCHMARK_THRESHOLD:
            return (
                STRONG_BENCHMARK_INTERPRETATION
            )

        if benchmark_score >= MODERATE_BENCHMARK_THRESHOLD:
            return (
                MODERATE_BENCHMARK_INTERPRETATION
            )

        return (
            WEAK_BENCHMARK_INTERPRETATION
        )