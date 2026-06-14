from __future__ import annotations

from src.domain.validators.schema_validator import SchemaValidator
from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError
from src.evaluation.reporting.schemas.visual_analytics_snapshot_schema import VISUAL_ANALYTICS_SNAPSHOT_SCHEMA


class VisualAnalyticsSnapshotValidator:
    """VisualAnalyticsSnapshot validation service."""

    @staticmethod
    def validate(**values: object) -> None:
        SchemaValidator.validate(
            values=dict(values),
            schema=VISUAL_ANALYTICS_SNAPSHOT_SCHEMA,
            error_factory=EvaluationValidationError,
        )
