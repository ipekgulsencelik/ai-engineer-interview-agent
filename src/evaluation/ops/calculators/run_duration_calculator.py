from __future__ import annotations

from datetime import datetime


class RunDurationCalculator:
    """
    Run duration calculator.
    """

    @staticmethod
    def calculate(
        *,
        started_at: datetime,
        completed_at: datetime,
    ) -> float:
        return (
            completed_at
            - started_at
        ).total_seconds()