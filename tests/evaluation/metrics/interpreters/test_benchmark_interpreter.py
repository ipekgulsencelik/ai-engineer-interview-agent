from __future__ import annotations

from src.evaluation.metrics.interpreters.benchmark_interpreter import (
    BenchmarkInterpreter,
)


def test_benchmark_interpreter_should_return_strong_benchmark() -> None:
    assert (
        BenchmarkInterpreter.interpret(
            benchmark_score=0.85,
        )
        == "strong_benchmark"
    )


def test_benchmark_interpreter_should_return_moderate_benchmark() -> None:
    assert (
        BenchmarkInterpreter.interpret(
            benchmark_score=0.70,
        )
        == "moderate_benchmark"
    )


def test_benchmark_interpreter_should_return_weak_benchmark() -> None:
    assert (
        BenchmarkInterpreter.interpret(
            benchmark_score=0.40,
        )
        == "weak_benchmark"
    )