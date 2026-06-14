from __future__ import annotations

from enum import StrEnum


class ExperimentTrendDirection(
    StrEnum,
):
    """
    Experiment trend direction.
    """

    IMPROVING = "improving"

    REGRESSING = "regressing"

    STABLE = "stable"

    VOLATILE = "volatile"

    UNKNOWN = "unknown"