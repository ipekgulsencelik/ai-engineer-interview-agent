"""Lossless boundary mapper between delivery domain entity and schema DTO."""

from __future__ import annotations

from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)
from src.evaluation.reporting.schemas.report_delivery_result_schema import (
    ReportDeliveryResultSchema,
)


class ReportDeliveryResultMapper:
    """Mapping does not perform delivery I/O or mutate the input objects."""

    @staticmethod
    def to_schema(result: ReportDeliveryResult) -> ReportDeliveryResultSchema:
        return ReportDeliveryResultSchema(
            delivery_id=result.delivery_id,
            report_id=result.report_id,
            artifact_id=result.artifact_id,
            delivery_type=result.delivery_type,
            destination=result.destination,
            success=result.success,
            delivered_at=result.delivered_at,
            provider=result.provider,
            status_code=result.status_code,
            error_message=result.error_message,
            retry_count=result.retry_count,
            metadata=None if result.metadata is None else dict(result.metadata),
        )

    @staticmethod
    def from_schema(schema: ReportDeliveryResultSchema) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=schema.delivery_id,
            report_id=schema.report_id,
            artifact_id=schema.artifact_id,
            delivery_type=schema.delivery_type,
            destination=schema.destination,
            success=schema.success,
            delivered_at=schema.delivered_at,
            provider=schema.provider,
            status_code=schema.status_code,
            error_message=schema.error_message,
            retry_count=schema.retry_count,
            metadata=None if schema.metadata is None else dict(schema.metadata),
        )
