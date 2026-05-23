from __future__ import annotations

from src.infrastructure.models.benchmark_case import (
    BenchmarkCase,
)


class BenchmarkCaseMapper:
    """
    BenchmarkCase payload mapper.
    """

    @staticmethod
    def map(
        *,
        payload: dict[str, object],
    ) -> BenchmarkCase:
        return BenchmarkCase(
            query=str(payload["query"]),
            expected_category=str(
                payload["expected_category"],
            ),
        )