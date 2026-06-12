from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping

from src.evaluation.ops.enums.audit_action import (
    AuditAction,
)
from src.evaluation.ops.enums.audit_aggregate_type import (
    AuditAggregateType,
)
from src.evaluation.ops.enums.audit_event_type import (
    AuditEventType,
)
from src.evaluation.ops.enums.audit_trigger import (
    AuditTrigger,
)
from src.evaluation.ops.types.audit_metadata import (
    AuditMetadataValue,
)
from src.evaluation.ops.validators.audit_event_validator import (
    AuditEventValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AuditEvent:
    """
    Immutable audit event.

    Represents an operational evaluation event used for
    traceability, governance, debugging, and compliance.
    """

    event_id: str

    event_type: AuditEventType

    aggregate_id: str
    aggregate_type: AuditAggregateType

    benchmark_id: str
    experiment_id: str

    model_name: str

    occurred_at: datetime

    actor: str

    action: AuditAction

    triggered_by: AuditTrigger

    metadata: Mapping[
        str,
        AuditMetadataValue,
    ] = MappingProxyType({})

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        AuditEventValidator.validate(
            event_id=self.event_id,
            event_type=self.event_type,
            aggregate_id=self.aggregate_id,
            aggregate_type=self.aggregate_type,
            benchmark_id=self.benchmark_id,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            occurred_at=self.occurred_at,
            actor=self.actor,
            action=self.action,
            triggered_by=self.triggered_by,
            metadata=self.metadata,
            notes=self.notes,
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(
                dict(self.metadata)
            ),
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )