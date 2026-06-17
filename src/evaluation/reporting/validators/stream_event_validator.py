from __future__ import annotations

from datetime import datetime
from typing import Any

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.stream_event_schema import (
    STREAM_EVENT_SCHEMA,
)


class StreamEventValidator:
    """
    StreamEvent validation service.
    """

    @staticmethod
    def validate(
        *,
        event_id: str,
        stream_id: str,
        event_type: str,
        occurred_at: datetime,
        source: str,
        sequence_number: int,
        payload: dict[
            str,
            Any,
        ],
        correlation_id: str | None,
        trace_id: str | None,
        run_id: str | None,
        experiment_id: str | None,
        entity_type: str | None,
        entity_id: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "event_id": event_id,
                "stream_id": stream_id,
                "event_type": event_type,
                "occurred_at": occurred_at,
                "source": source,
                "sequence_number": sequence_number,
                "payload": payload,
                "correlation_id": correlation_id,
                "trace_id": trace_id,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "metadata": metadata or {},
            },
            schema=STREAM_EVENT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not payload:
            raise EvaluationValidationError(
                "payload cannot be empty."
            )

        if (
            entity_type is None
        ) != (
            entity_id is None
        ):
            raise EvaluationValidationError(
                "entity_type and entity_id must both be provided or both be None."
            )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )