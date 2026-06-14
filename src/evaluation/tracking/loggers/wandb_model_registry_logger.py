from __future__ import annotations

from pathlib import Path

import wandb

from src.evaluation.tracking.clients.wandb_run_initializer import (
    WandBRunInitializer,
)
from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)


class WandBModelRegistryLogger:
    """
    Logs model registry entries to W&B.
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
        model: ModelRegistryEntry,
    ) -> None:
        run = self._run_initializer.init(
            name=model.identifier,
            tags=(
                str(model.stage),
                model.model_name,
                model.model_version,
            ),
            config={
                "registry_id": model.registry_id,
                "model_name": model.model_name,
                "model_version": model.model_version,
                "stage": str(model.stage),
                "created_at": model.created_at.isoformat(),
                "framework": model.framework,
                "provider": model.provider,
                "model_uri": model.model_uri,
                "artifact_path": model.artifact_path,
                "checksum": model.checksum,
                "owner": model.owner,
                "description": model.description,
                "metadata": model.metadata or {},
                "benchmark_score": model.benchmark_score,
            },
        )

        try:
            if model.benchmark_score is not None:
                run.log(
                    {
                        "benchmark_score": (
                            model.benchmark_score
                        ),
                    }
                )

            if model.artifact_path is not None:
                path = Path(model.artifact_path)

                if path.exists() and path.is_file():
                    artifact = wandb.Artifact(
                        name=model.identifier.replace(
                            ":",
                            "-",
                        ),
                        type="model",
                        description=model.description,
                        metadata=model.metadata or {},
                    )
                    artifact.add_file(str(path))
                    run.log_artifact(artifact)
        finally:
            run.finish()