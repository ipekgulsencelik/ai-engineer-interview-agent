from __future__ import annotations

from src.infrastructure.models.benchmark_summary import (
    BenchmarkSummary,
)
from src.ui.presentation.benchmark_metric_item import (
    BenchmarkMetricItem,
)


class BenchmarkSummaryFormatter:
    """
    UI formatting utilities for BenchmarkSummary.
    """

    @staticmethod
    def to_metric_items(
        *,
        summary: BenchmarkSummary,
    ) -> list[BenchmarkMetricItem]:
        return [
            BenchmarkMetricItem(
                label="Queries",
                value=str(summary.total_queries),
            ),
            BenchmarkMetricItem(
                label="Hit Rate",
                value=(
                    f"{summary.category_hit_rate:.2%}"
                ),
            ),
            BenchmarkMetricItem(
                label="Avg Latency",
                value=(
                    f"{summary.average_latency_seconds:.4f}s"
                ),
            ),
            BenchmarkMetricItem(
                label="Avg Score",
                value=(
                    f"{summary.average_top_score:.4f}"
                ),
            ),
        ]