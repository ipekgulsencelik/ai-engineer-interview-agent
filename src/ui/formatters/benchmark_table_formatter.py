from __future__ import annotations

import pandas as pd

from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)


class BenchmarkTableFormatter:
    """
    Benchmark table dataframe formatter.
    """

    @staticmethod
    def to_dataframe(
        *,
        results: list[BenchmarkResult],
    ) -> pd.DataFrame:
        rows = [
            {
                "query": result.query,
                "expected_category": (
                    result.expected_category
                ),
                "top_question_id": (
                    result.top_question_id
                ),
                "top_score": result.top_score,
                "category_hit": (
                    result.category_hit
                ),
                "latency_seconds": (
                    result.latency_seconds
                ),
            }
            for result in results
        ]

        return pd.DataFrame(rows)