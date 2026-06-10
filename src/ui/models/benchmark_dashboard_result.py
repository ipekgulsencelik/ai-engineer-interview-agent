from __future__ import annotations

from dataclasses import dataclass

from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)
from src.infrastructure.models.benchmark_summary import (
    BenchmarkSummary,
)


@dataclass(frozen=True)
class BenchmarkDashboardResult:
    """
    Benchmark dashboard aggregate UI result.
    """

    summary: BenchmarkSummary

    results: list[BenchmarkResult]