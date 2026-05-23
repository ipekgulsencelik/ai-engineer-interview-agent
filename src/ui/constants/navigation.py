from __future__ import annotations

from typing import Final

from src.ui.enums.navigation_page import (
    NavigationPage,
)


SIDEBAR_TITLE: Final[str] = (
    "AI Interview Agent"
)

NAVIGATION_LABEL: Final[str] = (
    "Navigation"
)

NAVIGATION_OPTIONS: Final[list[NavigationPage]] = [
    NavigationPage.INTERVIEW,
    NavigationPage.CV_ANALYSIS,
    NavigationPage.BENCHMARK_DASHBOARD,
]