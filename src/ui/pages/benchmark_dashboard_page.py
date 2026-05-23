from __future__ import annotations

import streamlit as st

from src.ui.constants.benchmark_page_texts import (
    BENCHMARK_DASHBOARD_TITLE,
    RUN_RETRIEVAL_BENCHMARK_BUTTON_LABEL,
)
from src.ui.presenters.benchmark_dashboard_presenter import (
    BenchmarkDashboardPresenter,
)
from src.ui.services.benchmark_dashboard_service import (
    BenchmarkDashboardService,
)


class BenchmarkDashboardPage:
    """
    Retrieval benchmark analytics dashboard.
    """

    @staticmethod
    def render() -> None:
        st.title(
            BENCHMARK_DASHBOARD_TITLE,
        )

        if not st.button(
            RUN_RETRIEVAL_BENCHMARK_BUTTON_LABEL,
        ):
            return

        result = BenchmarkDashboardService.run()

        BenchmarkDashboardPresenter.render(
            result=result,
        )