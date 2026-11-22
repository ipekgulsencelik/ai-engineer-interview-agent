from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_OBJECT_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_validator import SchemaValidator
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REPORT_DELIVERY_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "delivery_id": NON_EMPTY_STRING_RULE,
    "report_id": NON_EMPTY_STRING_RULE,
    "artifact_id": NON_EMPTY_STRING_RULE,
    "delivery_type": NON_EMPTY_STRING_RULE,
    "destination": NON_EMPTY_STRING_RULE,
    "success": BOOLEAN_RULE,
    "delivered_at": DATETIME_OBJECT_RULE,
    "provider": OPTIONAL_STRING_RULE,
    "status_code": OPTIONAL_NUMBER_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "retry_count": NON_NEGATIVE_NUMBER_RULE,
    "metadata": DICT_RULE,
}

@dataclass(frozen=True, slots=True, kw_only=True)
class ReportDeliveryResultSchema:
    """Serializable delivery DTO; preserves all domain fields without I/O."""

    delivery_id: str
    report_id: str
    artifact_id: str
    delivery_type: str
    destination: str
    success: bool
    delivered_at: datetime
    provider: str | None = None
    status_code: int | None = None
    error_message: str | None = None
    retry_count: int = 0
    metadata: dict[str, str] | None = None

    def __post_init__(self) -> None:
        SchemaValidator.validate(
            values={
                "delivery_id": self.delivery_id,
                "report_id": self.report_id,
                "artifact_id": self.artifact_id,
                "delivery_type": self.delivery_type,
                "destination": self.destination,
                "success": self.success,
                "delivered_at": self.delivered_at,
                "provider": self.provider,
                "status_code": self.status_code,
                "error_message": self.error_message,
                "retry_count": self.retry_count,
                "metadata": self.metadata or {},
            },
            schema=REPORT_DELIVERY_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )
