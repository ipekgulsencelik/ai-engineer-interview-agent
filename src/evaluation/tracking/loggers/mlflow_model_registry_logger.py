from __future__ import annotations

import mlflow

from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)


class MLflowModelRegistryLogger:
    """
    Logs and registers model registry entries in MLflow.
    """

    @staticmethod
    def log(
        *,
        model: ModelRegistryEntry,
    ) -> None:
        with mlflow.start_run(
            run_name=model.identifier,
            nested=True,
        ):
            mlflow.set_tags(
                {
                    "registry_id": model.registry_id,
                    "model_name": model.model_name,
                    "model_version": model.model_version,
                    "stage": str(model.stage),
                    "created_at": model.created_at.isoformat(),
                    "framework": model.framework or "",
                    "provider": model.provider or "",
                    "model_uri": model.model_uri or "",
                    "artifact_path": model.artifact_path or "",
                    "checksum": model.checksum or "",
                    "owner": model.owner or "",
                }
            )

            if model.benchmark_score is not None:
                mlflow.log_metric(
                    "benchmark_score",
                    model.benchmark_score,
                )

            if model.metadata:
                mlflow.set_tags(
                    {
                        f"metadata.{key}": value
                        for key, value in model.metadata.items()
                    }
                )

            if model.tags:
                mlflow.set_tag(
                    "tags",
                    ",".join(model.tags),
                )

            if model.model_uri is not None:
                mlflow.register_model(
                    model_uri=model.model_uri,
                    name=model.model_name,
                )