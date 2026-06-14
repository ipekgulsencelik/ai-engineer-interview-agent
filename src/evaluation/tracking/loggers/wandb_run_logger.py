from __future__ import annotations

from src.evaluation.tracking.clients.wandb.wandb_run_initializer import (
    WandBRunInitializer,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class WandBRunLogger:
    """
    Logs experiment runs to W&B.
    """

    def __init__(
        self,
        *,
        run_initializer: WandBRunInitializer,
    ) -> None:
        self._run_initializer = run_initializer

    def log(
        self,
        *,
        run_entity: ExperimentRun,
    ) -> None:
        run = self._run_initializer.init(
            name=run_entity.run_id,
            tags=(
                str(run_entity.status),
                run_entity.experiment_name,
                run_entity.experiment_version,
            ),
            config={
                "run_id": run_entity.run_id,
                "experiment_id": run_entity.experiment_id,
                "experiment_name": run_entity.experiment_name,
                "experiment_version": run_entity.experiment_version,
                "dataset_id": run_entity.dataset_id,
                "dataset_name": run_entity.dataset_name,
                "dataset_version": run_entity.dataset_version,
                "benchmark_id": run_entity.benchmark_id,
                "benchmark_name": run_entity.benchmark_name,
                "benchmark_version": run_entity.benchmark_version,
                "model_name": run_entity.model_name,
                "retriever_name": run_entity.retriever_name,
                "evaluator_name": run_entity.evaluator_name,
                "status": str(run_entity.status),
                "started_at": run_entity.started_at.isoformat(),
                "completed_at": (
                    None
                    if run_entity.completed_at is None
                    else run_entity.completed_at.isoformat()
                ),
                "notes": run_entity.notes,
            },
        )

        try:
            run.log(
                {
                    key: value
                    for key, value in {
                        "overall_score": run_entity.overall_score,
                        "pass_rate": run_entity.pass_rate,
                        "sample_count": run_entity.sample_count,
                        "passed_count": run_entity.passed_count,
                        "failed_count": run_entity.failed_count,
                        "duration_ms": run_entity.duration_ms,
                    }.items()
                    if value is not None
                }
            )
        finally:
            run.finish()