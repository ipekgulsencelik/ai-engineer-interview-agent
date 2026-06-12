from __future__ import annotations

from typing import Final


DASHBOARD_METRIC_CARDS_TYPE_ERROR: Final[
    str
] = (
    "metric_cards must be tuple."
)

DASHBOARD_METRIC_CARD_TYPE_ERROR: Final[
    str
] = (
    "metric_cards item must be DashboardMetricCard."
)

DASHBOARD_TREND_POINTS_TYPE_ERROR: Final[
    str
] = (
    "trend_points must be tuple."
)

DASHBOARD_TREND_POINT_TYPE_ERROR: Final[
    str
] = (
    "trend_points item must be DashboardTrendPoint."
)

DASHBOARD_DUPLICATE_METRIC_CARD_ID_ERROR: Final[
    str
] = (
    "metric_cards contains duplicate card_id."
)

DASHBOARD_TREND_POINT_ORDER_ERROR: Final[
    str
] = (
    "trend_points must be ordered by occurred_at."
)