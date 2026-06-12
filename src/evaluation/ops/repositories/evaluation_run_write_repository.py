from __future__ import annotations

from abc import ABC, abstractmethod

from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class EvaluationRunWriteRepository(
    ABC,
):
    """
    Write repository contract for evaluation runs.
    """

    @abstractmethod
    def save(
        self,
        *,
        result: EvaluationRunResult,
    ) -> None:
        raise NotImplementedError