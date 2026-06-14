from __future__ import annotations

import asyncio

import mlflow

from src.evaluation.tracking.clients.external_tracking_client import (
    ExternalTrackingClient,
)
from src.evaluation.tracking.loggers.mlflow_artifact_logger import (
    MLflowArtifactLogger,
)
from src.evaluation.tracking.loggers.mlflow_event_logger import (
    MLflowEventLogger,
)
from src.evaluation.tracking.loggers.mlflow_model_registry_logger import (
    MLflowModelRegistryLogger,
)
from src.evaluation.tracking.loggers.mlflow_run_logger import (
    MLflowRunLogger,
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


class MLflowTrackingClient(
    ExternalTrackingClient,
):
    """
    MLflow implementation of ExternalTrackingClient.
    """

    def __init__(
        self,
        *,
        tracking_uri: str | None = None,
        experiment_name: str | None = None,
        event_logger: MLflowEventLogger | None = None,
        run_logger: MLflowRunLogger | None = None,
        artifact_logger: MLflowArtifactLogger | None = None,
        model_registry_logger: (
            MLflowModelRegistryLogger | None
        ) = None,
    ) -> None:
        if tracking_uri is not None:
            mlflow.set_tracking_uri(
                tracking_uri,
            )

        if experiment_name is not None:
            mlflow.set_experiment(
                experiment_name,
            )

        self._event_logger = (
            event_logger
            or MLflowEventLogger()
        )
        self._run_logger = (
            run_logger
            or MLflowRunLogger()
        )
        self._artifact_logger = (
            artifact_logger
            or MLflowArtifactLogger()
        )
        self._model_registry_logger = (
            model_registry_logger
            or MLflowModelRegistryLogger()
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
            run=run,
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
        return None