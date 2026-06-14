from __future__ import annotations

from pathlib import Path

import mlflow

from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)


class MLflowArtifactLogger:
    """
    Logs experiment artifacts to MLflow.
    """

    @staticmethod
    def log(
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        with mlflow.start_run(
            run_name=artifact.run_id,
            nested=True,
        ):
            mlflow.set_tags(
                {
                    "artifact_id": artifact.artifact_id,
                    "artifact_type": str(artifact.artifact_type),
                    "artifact_name": artifact.artifact_name,
                    "artifact_path": artifact.artifact_path,
                    "artifact_uri": artifact.artifact_uri or "",
                    "storage_backend": artifact.storage_backend or "",
                    "content_type": artifact.content_type,
                    "checksum": artifact.checksum or "",
                    "created_at": artifact.created_at.isoformat(),
                }
            )

            if artifact.size_bytes is not None:
                mlflow.log_metric(
                    "artifact_size_bytes",
                    float(artifact.size_bytes),
                )

            path = Path(
                artifact.artifact_path,
            )

            if path.exists() and path.is_file():
                mlflow.log_artifact(
                    local_path=str(path),
                )