from __future__ import annotations

import asyncio

import wandb

from src.evaluation.tracking.clients.external_tracking_client import (
    ExternalTrackingClient,
)
from src.evaluation.tracking.loggers.wandb.wandb_artifact_logger import (
    WandBArtifactLogger,
)
from src.evaluation.tracking.loggers.wandb.wandb_event_logger import (
    WandBEventLogger,
)
from src.evaluation.tracking.loggers.wandb.wandb_model_registry_logger import (
    WandBModelRegistryLogger,
)
from src.evaluation.tracking.initializers.wandb.wandb_run_initializer import (
    WandBRunInitializer,
)
from src.evaluation.tracking.loggers.wandb.wandb_run_logger import (
    WandBRunLogger,
)
from src.evaluation.tracking.entities.experiment_artifact import (
    ExperimentArtifact,
)
from src.evaluation.tracking.entities.experiment_run import (
    ExperimentRun,
)
from src.evaluation.tracking.entities.model_registry_entry import (
    ModelRegistryEntry,
)
from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)


class WandBTrackingClient(
    ExternalTrackingClient,
):
    """
    Weights & Biases implementation of ExternalTrackingClient.
    """

    def __init__(
        self,
        *,
        project: str,
        entity: str | None = None,
        group: str | None = None,
        job_type: str | None = None,
        mode: str | None = None,
        run_initializer: WandBRunInitializer | None = None,
        event_logger: WandBEventLogger | None = None,
        run_logger: WandBRunLogger | None = None,
        artifact_logger: WandBArtifactLogger | None = None,
        model_registry_logger: (
            WandBModelRegistryLogger | None
        ) = None,
    ) -> None:
        self._run_initializer = (
            run_initializer
            or WandBRunInitializer(
                project=project,
                entity=entity,
                group=group,
                job_type=job_type,
                mode=mode,
            )
        )

        self._event_logger = (
            event_logger
            or WandBEventLogger(
                run_initializer=self._run_initializer,
            )
        )

        self._run_logger = (
            run_logger
            or WandBRunLogger(
                run_initializer=self._run_initializer,
            )
        )

        self._artifact_logger = (
            artifact_logger
            or WandBArtifactLogger(
                run_initializer=self._run_initializer,
            )
        )

        self._model_registry_logger = (
            model_registry_logger
            or WandBModelRegistryLogger(
                run_initializer=self._run_initializer,
            )
        )

    async def log_event(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        await asyncio.to_thread(
            self._event_logger.log,
            event=event,
        )

    async def log_run(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        await asyncio.to_thread(
            self._run_logger.log,
            run_entity=run,
        )

    async def update_run(
        self,
        *,
        run: ExperimentRun,
    ) -> None:
        await self.log_run(
            run=run,
        )

    async def log_artifact(
        self,
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        await asyncio.to_thread(
            self._artifact_logger.log,
            artifact=artifact,
        )

    async def upload_artifact(
        self,
        *,
        artifact: ExperimentArtifact,
    ) -> None:
        await self.log_artifact(
            artifact=artifact,
        )

    async def register_model(
        self,
        *,
        model: ModelRegistryEntry,
    ) -> None:
        await asyncio.to_thread(
            self._model_registry_logger.log,
            model=model,
        )

    async def close(
        self,
    ) -> None:
        await asyncio.to_thread(
            wandb.finish,
        )