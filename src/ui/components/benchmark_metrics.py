from __future__ import annotations

import streamlit as st

from src.infrastructure.models.benchmark_summary import (
    BenchmarkSummary,
)
from src.ui.formatters.benchmark_summary_formatter import (
    BenchmarkSummaryFormatter,
)


class BenchmarkMetrics:
    """
    Benchmark KPI visualization component.
    """

    @staticmethod
    def render(
        *,
        summary: BenchmarkSummary,
    ) -> None:
        metric_items = (
            BenchmarkSummaryFormatter.to_metric_items(
                summary=summary,
            )
        )

        columns = st.columns(
            len(metric_items),
        )

        for column, item in zip(
            columns,
            metric_items,
            strict=True,
        ):
            column.metric(
                item.label,
                item.value,
            )