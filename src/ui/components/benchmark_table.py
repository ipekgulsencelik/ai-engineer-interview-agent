from __future__ import annotations

import streamlit as st

from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)
from src.ui.formatters.benchmark_table_formatter import (
    BenchmarkTableFormatter,
)


class BenchmarkTable:
    """
    Benchmark result table renderer.
    """

    @staticmethod
    def render(
        *,
        results: list[BenchmarkResult],
    ) -> None:
        dataframe = (
            BenchmarkTableFormatter.to_dataframe(
                results=results,
            )
        )

        st.dataframe(
            dataframe,
            use_container_width=True,
        )