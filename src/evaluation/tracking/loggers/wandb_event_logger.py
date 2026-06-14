from __future__ import annotations

from src.evaluation.ops.clients.wandb.wandb_payload_mapper import (
    WandBPayloadMapper,
)
from src.evaluation.ops.clients.wandb.wandb_run_initializer import (
    WandBRunInitializer,
)
from src.evaluation.ops.entities.tracking_event import (
    TrackingEvent,
)


class WandBEventLogger:
    """
    Logs tracking events to W&B.
    """

    def __init__(
        self,
        *,
        run_initializer: WandBRunInitializer,
        payload_mapper: WandBPayloadMapper | None = None,
    ) -> None:
        self._run_initializer = run_initializer
        self._payload_mapper = payload_mapper or WandBPayloadMapper()

    def log(
        self,
        *,
        event: TrackingEvent,
    ) -> None:
        run = self._run_initializer.init(
            name=event.entity_id,
            tags=(
                event.event_type,
                event.entity_type,
            ),
            config={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "source": event.source,
                "entity_type": event.entity_type,
                "entity_id": event.entity_id,
                "actor": event.actor,
                "run_id": event.run_id,
                "experiment_id": event.experiment_id,
                "correlation_id": event.correlation_id,
                "trace_id": event.trace_id,
                "occurred_at": event.occurred_at.isoformat(),
                "description": event.description,
                "metadata": event.metadata or {},
            },
        )

        try:
            run.log(
                {
                    "event": {
                        "event_id": event.event_id,
                        "event_type": event.event_type,
                        "source": event.source,
                        "entity_type": event.entity_type,
                        "entity_id": event.entity_id,
                        "payload": event.payload or {},
                        "metadata": event.metadata or {},
                    }
                }
            )

            if event.payload:
                run.log(
                    self._payload_mapper.numeric_payload(
                        payload=event.payload,
                    )
                )
        finally:
            run.finish()