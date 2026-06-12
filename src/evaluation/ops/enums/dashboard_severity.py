from __future__ import annotations 

from enum import StrEnum 


class DashboardSeverity(StrEnum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    CRITICAL = "critical"