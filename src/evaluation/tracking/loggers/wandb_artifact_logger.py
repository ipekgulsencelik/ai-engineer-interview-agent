from __future__ import annotations

from pathlib import Path

import wandb

from src.evaluation.tracking.clients.wandb_run_initializer import (
    WandBRunInitializer,
)
from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)


class WandBArtifactLogger:
    """
    Logs experiment artifacts to W&B.
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
        artifact: ExperimentArtifact,
    ) -> None:
        run = self._run_initializer.init(
            name=artifact.run_id,
            tags=(
                str(artifact.artifact_type),
                artifact.content_type,
            ),
            config={
                "artifact_id": artifact.artifact_id,
                "run_id": artifact.run_id,
                "experiment_id": artifact.experiment_id,
                "artifact_type": str(artifact.artifact_type),
                "artifact_name": artifact.artifact_name,
                "artifact_path": artifact.artifact_path,
                "artifact_uri": artifact.artifact_uri,
                "storage_backend": artifact.storage_backend,
                "content_type": artifact.content_type,
                "size_bytes": artifact.size_bytes,
                "checksum": artifact.checksum,
                "created_at": artifact.created_at.isoformat(),
                "description": artifact.description,
                "metadata": artifact.metadata or {},
            },
        )

        try:
            path = Path(
                artifact.artifact_path,
            )

            if path.exists() and path.is_file():
                wandb_artifact = wandb.Artifact(
                    name=artifact.artifact_name,
                    type=str(artifact.artifact_type),
                    description=artifact.description,
                    metadata=artifact.metadata or {},
                )
                wandb_artifact.add_file(str(path))
                run.log_artifact(wandb_artifact)

            if artifact.size_bytes is not None:
                run.log(
                    {
                        "artifact_size_bytes": (
                            artifact.size_bytes
                        ),
                    }
                )
        finally:
            run.finish()