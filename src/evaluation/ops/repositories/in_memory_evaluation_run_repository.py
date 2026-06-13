from __future__ import annotations

from src.evaluation.ops.repositories.evaluation_run_repository import (
    EvaluationRunRepository,
)
from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class InMemoryEvaluationRunRepository(
    EvaluationRunRepository,
):
    """
    In-memory evaluation run repository.
    """

    def __init__(
        self,
    ) -> None:
        self._results: dict[
            str,
            EvaluationRunResult,
        ] = {}

    def save(
        self,
        *,
        result: EvaluationRunResult,
    ) -> None:
        self._results[
            result.run_id
        ] = result

    def find_by_run_id(
        self,
        *,
        run_id: str,
    ) -> EvaluationRunResult | None:
        return self._results.get(
            run_id,
        )

    def find_by_experiment_id(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        return tuple(
            result
            for result in self._results.values()
            if (
                result.experiment_id
                == experiment_id
            )
        )

    def find_by_benchmark_id(
        self,
        *,
        benchmark_id: str,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        return tuple(
            result
            for result in self._results.values()
            if (
                result.benchmark_id
                == benchmark_id
            )
        )

    def list_recent(
        self,
        *,
        limit: int,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        return tuple(
            sorted(
                self._results.values(),
                key=lambda result: (
                    result.completed_at
                ),
                reverse=True,
            )[:limit]
        )

    def clear(
        self,
    ) -> None:
        self._results.clear()