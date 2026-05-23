from __future__ import annotations

from src.ui.components.sidebar import (
    Sidebar,
)
from src.ui.enums.navigation_page import (
    NavigationPage,
)
from src.ui.pages.cv_analysis_page import (
    CVAnalysisPage,
)
from src.ui.pages.benchmark_dashboard_page import (
    BenchmarkDashboardPage,
)
from src.ui.pages.interview_page import (
    InterviewPage,
)


page = Sidebar.render()

if page == NavigationPage.INTERVIEW:
    InterviewPage.render()

elif page == NavigationPage.CV_ANALYSIS:
    CVAnalysisPage.render()

elif page == NavigationPage.BENCHMARK_DASHBOARD:
    BenchmarkDashboardPage.render()