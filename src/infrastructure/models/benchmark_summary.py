from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkSummary:
    """
    Benchmark aggregate summary snapshot.
    """

    total: float

    category_hit_rate: float

    average_latency_seconds: float

    average_top_score: float