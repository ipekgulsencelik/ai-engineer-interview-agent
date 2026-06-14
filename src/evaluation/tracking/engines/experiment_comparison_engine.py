from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.repositories.experiment_run_repository import (
    ExperimentRunRepository,
)
from src.evaluation.ops.services.experiment_comparison_service import (
    ExperimentComparisonService,
)
from src.evaluation.ops.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)


class ExperimentComparisonEngine:
    """
    Application service for comparing experiment runs.

    Loads baseline and candidate runs from repository,
    delegates metric comparison to ExperimentComparisonService,
    and returns an immutable comparison result.
    """

    def __init__(
        self,
        *,
        run_repository: ExperimentRunRepository,
        comparison_service: ExperimentComparisonService | None = None,
    ) -> None:
        self._run_repository = run_repository
        self._comparison_service = (
            comparison_service
            or ExperimentComparisonService()
        )

    def compare_runs(
        self,
        *,
        baseline_run_id: str,
        candidate_run_id: str,
        notes: str | None = None,
    ) -> ExperimentComparisonResult:
        if baseline_run_id == candidate_run_id:
            raise EvaluationValidationError(
                "baseline_run_id cannot equal candidate_run_id."
            )

        baseline = self._run_repository.get_by_id(
            run_id=baseline_run_id,
        )

        if baseline is None:
            raise EvaluationValidationError(
                "baseline experiment run not found."
            )

        candidate = self._run_repository.get_by_id(
            run_id=candidate_run_id,
        )

        if candidate is None:
            raise EvaluationValidationError(
                "candidate experiment run not found."
            )

        return self._comparison_service.compare(
            baseline=baseline,
            candidate=candidate,
            notes=notes,
        )