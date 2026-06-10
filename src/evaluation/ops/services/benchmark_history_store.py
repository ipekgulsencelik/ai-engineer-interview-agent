from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.benchmark_history import (
    BenchmarkHistory,
)


class BenchmarkHistoryStore:
    """
    In-memory benchmark history store.

    Stores benchmark histories by benchmark identity.
    """

    def __init__(
        self,
    ) -> None:
        self._histories: dict[
            str,
            BenchmarkHistory,
        ] = {}

    def save(
        self,
        *,
        history: BenchmarkHistory,
    ) -> None:
        self._histories[
            self._build_key(
                benchmark_id=history.benchmark_id,
                benchmark_version=history.benchmark_version,
            )
        ] = history

    def get(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
    ) -> BenchmarkHistory:
        key = self._build_key(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
        )

        try:
            return self._histories[key]
        except KeyError as exc:
            raise EvaluationValidationError(
                "benchmark history is not found."
            ) from exc

    def contains(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
    ) -> bool:
        return (
            self._build_key(
                benchmark_id=benchmark_id,
                benchmark_version=benchmark_version,
            )
            in self._histories
        )

    def list_all(
        self,
    ) -> tuple[BenchmarkHistory, ...]:
        return tuple(
            self._histories.values(),
        )

    def delete(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
    ) -> None:
        key = self._build_key(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
        )

        if key not in self._histories:
            raise EvaluationValidationError(
                "benchmark history is not found."
            )

        del self._histories[key]

    def clear(
        self,
    ) -> None:
        self._histories.clear()

    @staticmethod
    def _build_key(
        *,
        benchmark_id: str,
        benchmark_version: str,
    ) -> str:
        return f"{benchmark_id}:{benchmark_version}"