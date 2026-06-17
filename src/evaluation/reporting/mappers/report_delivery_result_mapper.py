from __future__ import annotations

from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)
from src.evaluation.reporting.schemas.report_delivery_result_schema import (
    ReportDeliveryResultSchema,
)


class ReportDeliveryResultMapper:
    @staticmethod
    def to_schema(
        result: ReportDeliveryResult,
    ) -> ReportDeliveryResultSchema:
        return ReportDeliveryResultSchema(
            delivery_id=result.delivery_id,
            report_id=result.report_id,
            destination=result.destination,
            delivery_type=result.delivery_type,
            success=result.success,
            delivered_at=result.delivered_at,
            error_message=result.error_message,
            metadata=(
                None
                if result.metadata is None
                else dict(
                    result.metadata,
                )
            ),
        )

    @staticmethod
    def from_schema(
        schema: ReportDeliveryResultSchema,
    ) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=schema.delivery_id,
            report_id=schema.report_id,
            destination=schema.destination,
            delivery_type=schema.delivery_type,
            success=schema.success,
            delivered_at=schema.delivered_at,
            error_message=schema.error_message,
            metadata=schema.metadata,
        )