from __future__ import annotations

import mlflow

from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)


class MLflowRunLogger:
    """
    Logs experiment runs to MLflow.
    """

    @staticmethod
    def log(
        *,
        run: ExperimentRun,
    ) -> None:
        with mlflow.start_run(
            run_name=run.run_id,
            nested=True,
        ):
            mlflow.set_tags(
                {
                    "run_id": run.run_id,
                    "experiment_id": run.experiment_id,
                    "experiment_name": run.experiment_name,
                    "experiment_version": run.experiment_version,
                    "status": str(run.status),
                    "started_at": run.started_at.isoformat(),
                    "completed_at": (
                        ""
                        if run.completed_at is None
                        else run.completed_at.isoformat()
                    ),
                }
            )

            mlflow.log_params(
                {
                    key: value
                    for key, value in {
                        "dataset_id": run.dataset_id,
                        "dataset_name": run.dataset_name,
                        "dataset_version": run.dataset_version,
                        "benchmark_id": run.benchmark_id,
                        "benchmark_name": run.benchmark_name,
                        "benchmark_version": run.benchmark_version,
                        "model_name": run.model_name,
                        "retriever_name": run.retriever_name,
                        "evaluator_name": run.evaluator_name,
                    }.items()
                    if value is not None
                }
            )

            mlflow.log_metrics(
                {
                    key: float(value)
                    for key, value in {
                        "overall_score": run.overall_score,
                        "pass_rate": run.pass_rate,
                        "sample_count": run.sample_count,
                        "passed_count": run.passed_count,
                        "failed_count": run.failed_count,
                        "duration_ms": run.duration_ms,
                    }.items()
                    if value is not None
                }
            )

            if run.notes is not None:
                mlflow.set_tag(
                    "notes",
                    run.notes,
                )