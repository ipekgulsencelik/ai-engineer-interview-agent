from __future__ import annotations

import streamlit as st

from src.ui.components.benchmark_metrics import (
    BenchmarkMetrics,
)
from src.ui.components.benchmark_table import (
    BenchmarkTable,
)
from src.ui.models.benchmark_dashboard_result import (
    BenchmarkDashboardResult,
)


class BenchmarkDashboardPresenter:
    """
    Benchmark dashboard presentation orchestrator.
    """

    @staticmethod
    def render(
        *,
        result: BenchmarkDashboardResult,
    ) -> None:
        BenchmarkMetrics.render(
            summary=result.summary,
        )

        st.divider()

        BenchmarkTable.render(
            results=result.results,
        )