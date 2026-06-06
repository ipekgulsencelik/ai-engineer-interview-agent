from __future__ import annotations

from src.ui.components.sidebar import (
    Sidebar,
)
from src.ui.enums.navigation_page import (
    NavigationPage,
)


page = Sidebar.render()


if page == NavigationPage.INTERVIEW:
    from src.ui.pages.interview_page import InterviewPage

    InterviewPage.render()

elif page == NavigationPage.CV_ANALYSIS:
    from src.ui.pages.cv_analysis_page import CVAnalysisPage

    CVAnalysisPage.render()

elif page == NavigationPage.BENCHMARK_DASHBOARD:
    from src.ui.pages.benchmark_dashboard_page import BenchmarkDashboardPage

    BenchmarkDashboardPage.render()