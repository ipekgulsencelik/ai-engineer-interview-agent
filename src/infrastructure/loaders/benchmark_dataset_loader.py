from __future__ import annotations

import json
from pathlib import Path

from src.infrastructure.mappers.benchmark_case_mapper import (
    BenchmarkCaseMapper,
)
from src.infrastructure.benchmarking.models.benchmark_case import (
    BenchmarkCase,
)


class BenchmarkDatasetLoader:
    """
    Benchmark dataset JSON loader.
    """

    def load(
        self,
        file_path: str | Path,
    ) -> list[BenchmarkCase]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Benchmark dataset not found: {path}",
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            payload = json.load(file)

        if not isinstance(payload, list):
            raise TypeError(
                "Benchmark dataset root must be a list.",
            )

        cases: list[BenchmarkCase] = []

        for item in payload:
            if not isinstance(item, dict):
                raise TypeError(
                    "Benchmark dataset item "
                    "must be an object.",
                )

            cases.append(
                BenchmarkCaseMapper.map(
                    payload=item,
                )
            )

        return cases