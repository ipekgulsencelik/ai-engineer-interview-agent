from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.repositories.experiment_run_repository import (
    ExperimentRunRepository,
)


class ExperimentRegistry:
    """
    Registry service for experiment metadata and runs.

    Coordinates experiment node registration with
    run persistence. This service intentionally stays
    storage-agnostic by depending on repository ports.
    """

    def __init__(
        self,
        *,
        run_repository: ExperimentRunRepository,
    ) -> None:
        self._run_repository = run_repository

    def register_run(
        self,
        *,
        run: ExperimentRun,
    ) -> ExperimentRun:
        if self._run_repository.exists(
            run_id=run.run_id,
        ):
            raise EvaluationValidationError(
                "experiment run already exists."
            )

        self._run_repository.save(
            run=run,
        )

        return run

    def update_run(
        self,
        *,
        run: ExperimentRun,
    ) -> ExperimentRun:
        if not self._run_repository.exists(
            run_id=run.run_id,
        ):
            raise EvaluationValidationError(
                "experiment run does not exist."
            )

        self._run_repository.update(
            run=run,
        )

        return run

    def get_run(
        self,
        *,
        run_id: str,
    ) -> ExperimentRun | None:
        return self._run_repository.get_by_id(
            run_id=run_id,
        )

    def list_runs(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        ExperimentRun,
        ...,
    ]:
        return self._run_repository.list_by_experiment(
            experiment_id=experiment_id,
        )

    def create_node_from_run(
        self,
        *,
        run: ExperimentRun,
        parent_experiment_id: str | None = None,
        tags: tuple[
            str,
            ...,
        ] = (),
    ) -> ExperimentNode:
        return ExperimentNode(
            experiment_id=run.experiment_id,
            experiment_name=run.experiment_name,
            experiment_version=run.experiment_version,
            parent_experiment_id=parent_experiment_id,
            dataset_id=run.dataset_id,
            dataset_name=run.dataset_name,
            dataset_version=run.dataset_version,
            benchmark_id=run.benchmark_id,
            benchmark_name=run.benchmark_name,
            benchmark_version=run.benchmark_version,
            model_name=run.model_name,
            retriever_name=run.retriever_name,
            evaluator_name=run.evaluator_name,
            overall_score=run.overall_score,
            pass_rate=run.pass_rate,
            sample_count=run.sample_count,
            passed_count=run.passed_count,
            failed_count=run.failed_count,
            tags=tags,
            created_at=run.started_at,
            notes=run.notes,
        )