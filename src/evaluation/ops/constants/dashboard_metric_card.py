from __future__ import annotations

from typing import Final


DASHBOARD_SEVERITY_TYPE_ERROR: Final[
    str
] = (
    "severity must be DashboardSeverity."
)

TREND_VALUE_LABEL_MISMATCH_ERROR: Final[
    str
] = (
    "trend_label requires trend_value."
)

NEGATIVE_SORT_ORDER_ERROR: Final[
    str
] = (
    "sort_order cannot be negative."
)