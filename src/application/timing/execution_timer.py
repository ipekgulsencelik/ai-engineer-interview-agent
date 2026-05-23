from __future__ import annotations

import time


class ExecutionTimer:
    """
    Simple execution timer.
    """

    @staticmethod
    def current_timestamp() -> float:
        return time.perf_counter()

    @staticmethod
    def elapsed_since(
        *,
        started_at: float,
    ) -> float:
        return time.perf_counter() - started_at