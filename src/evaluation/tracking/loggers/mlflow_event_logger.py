from __future__ import annotations

import mlflow

from src.evaluation.tracking.clients.mlflow_payload_logger import (
    MLflowPayloadLogger,
)
from src.evaluation.tracking.entities.tracking_event import (
    TrackingEvent,
)


class MLflowEventLogger:
    """
    Logs tracking events to MLflow.
    """

    def __init__(
        self,
        *,
        payload_logger: MLflowPayloadLogger | None = None,
    ) -> None:
        self._payload_logger = (
            payload_logger
            or MLflowPayloadLogger()
        )

    def log(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        with mlflow.start_run(
            run_name=event.entity_id,
            nested=True,
        ):
            mlflow.set_tags(
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "source": event.source,
                    "entity_type": event.entity_type,
                    "entity_id": event.entity_id,
                    "actor": event.actor or "",
                    "run_id": event.run_id or "",
                    "experiment_id": event.experiment_id or "",
                    "correlation_id": event.correlation_id or "",
                    "trace_id": event.trace_id or "",
                    "occurred_at": event.occurred_at.isoformat(),
                }
            )

            if event.description is not None:
                mlflow.set_tag(
                    "description",
                    event.description,
                )

            if event.metadata:
                mlflow.set_tags(
                    {
                        f"metadata.{key}": value
                        for key, value in event.metadata.items()
                    }
                )

            if event.payload:
                self._payload_logger.log(
                    payload=event.payload,
                )