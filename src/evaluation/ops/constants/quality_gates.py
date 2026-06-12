from __future__ import annotations

from typing import Final


QUALITY_GATE_INFO_SEVERITY: Final[str] = "info"
QUALITY_GATE_WARNING_SEVERITY: Final[str] = "warning"
QUALITY_GATE_CRITICAL_SEVERITY: Final[str] = "critical"


VALID_QUALITY_GATE_SEVERITIES: Final[frozenset[str]] = frozenset(
    {
        QUALITY_GATE_INFO_SEVERITY,
        QUALITY_GATE_WARNING_SEVERITY,
        QUALITY_GATE_CRITICAL_SEVERITY,
    }
)