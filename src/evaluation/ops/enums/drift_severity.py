from __future__ import annotations

from enum import StrEnum


class DriftSeverity(
    StrEnum,
):
    INFO = "info"

    WARNING = "warning"

    CRITICAL = "critical"