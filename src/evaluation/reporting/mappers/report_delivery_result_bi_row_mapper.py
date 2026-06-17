from __future__ import annotations

from typing import Any

from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class ReportDeliveryResultBIRowMapper:
    """
    Maps report delivery results to BI rows.
    """

    def to_row(
        self,
        *,
        result: ReportDeliveryResult,
    ) -> dict[
        str,
        Any,
    ]:
        row = {
            "delivery_id": result.delivery_id,
            "report_id": result.report_id,
            "artifact_id": result.artifact_id,
            "delivery_type": result.delivery_type,
            "destination": result.destination,
            "success": result.success,
            "delivered_at": result.delivered_at.isoformat(),
            "provider": result.provider,
            "status_code": result.status_code,
            "error_message": result.error_message,
            "retry_count": result.retry_count,
        }

        if result.metadata:
            for key, value in result.metadata.items():
                row[
                    f"metadata_{key}"
                ] = value

        return row

    def to_rows(
        self,
        *,
        results: tuple[
            ReportDeliveryResult,
            ...,
        ],
    ) -> tuple[
        dict[
            str,
            Any,
        ],
        ...,
    ]:
        return tuple(
            self.to_row(
                result=result,
            )
            for result in results
        )