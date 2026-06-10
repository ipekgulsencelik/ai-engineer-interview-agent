from __future__ import annotations

from enum import StrEnum


class NavigationPage(StrEnum):
    """
    Sidebar navigation page options.
    """

    INTERVIEW = "Interview"
    CV_ANALYSIS = "CV Analysis"
    BENCHMARK_DASHBOARD = "Benchmark Dashboard"