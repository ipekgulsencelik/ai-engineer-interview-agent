from __future__ import annotations

from src.evaluation.ops.repositories.evaluation_run_read_repository import (
    EvaluationRunReadRepository,
)
from src.evaluation.ops.repositories.evaluation_run_write_repository import (
    EvaluationRunWriteRepository,
)
from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class InMemoryEvaluationRunRepository(
    EvaluationRunReadRepository,
    EvaluationRunWriteRepository,
):
    """
    In-memory repository for evaluation run results.

    Intended for tests, local development, and non-persistent
    evaluation workflows.
    """

    def __init__(
        self,
    ) -> None:
        self._results_by_run_id: dict[
            str,
            EvaluationRunResult,
        ] = {}

    def save(
        self,
        *,
        result: EvaluationRunResult,
    ) -> None:
        self._results_by_run_id[
            result.run_id
        ] = result

    def find_by_run_id(
        self,
        *,
        run_id: str,
    ) -> EvaluationRunResult | None:
        return self._results_by_run_id.get(
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
            for result in self._results_by_run_id.values()
            if result.experiment_id == experiment_id
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
            for result in self._results_by_run_id.values()
            if result.benchmark_id == benchmark_id
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
                self._results_by_run_id.values(),
                key=lambda result: result.completed_at,
                reverse=True,
            )[:limit]
        )

    def list_all(
        self,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        return tuple(
            self._results_by_run_id.values(),
        )