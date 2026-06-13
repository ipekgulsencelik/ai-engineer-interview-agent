from __future__ import annotations

from abc import ABC, abstractmethod

from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class EvaluationRunReadRepository(
    ABC,
):
    """
    Read repository contract for evaluation runs.
    """

    @abstractmethod
    def find_by_run_id(
        self,
        *,
        run_id: str,
    ) -> EvaluationRunResult | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_experiment_id(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        raise NotImplementedError

    @abstractmethod
    def find_by_benchmark_id(
        self,
        *,
        benchmark_id: str,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        raise NotImplementedError

    @abstractmethod
    def list_recent(
        self,
        *,
        limit: int,
    ) -> tuple[
        EvaluationRunResult,
        ...,
    ]:
        raise NotImplementedError
