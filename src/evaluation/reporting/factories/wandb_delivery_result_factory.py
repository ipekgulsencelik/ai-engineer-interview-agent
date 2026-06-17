from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class WandbDeliveryResultFactory:
    """
    Factory for creating W&B report delivery results.
    """

    DELIVERY_TYPE = "wandb"

    def create_success(
        self,
        *,
        report: ReportArtifact,
        destination: str,
        provider: str,
        delivered_at: datetime,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=str(
                uuid4(),
            ),
            report_id=report.report_id,
            artifact_id=report.artifact_id,
            delivery_type=self.DELIVERY_TYPE,
            destination=destination,
            success=True,
            delivered_at=delivered_at,
            provider=provider,
            status_code=200,
            error_message=None,
            retry_count=retry_count,
            metadata=self._delivery_metadata(
                report=report,
            ),
        )

    def create_failure(
        self,
        *,
        report: ReportArtifact,
        destination: str,
        provider: str,
        delivered_at: datetime,
        error_message: str,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=str(
                uuid4(),
            ),
            report_id=report.report_id,
            artifact_id=report.artifact_id,
            delivery_type=self.DELIVERY_TYPE,
            destination=destination,
            success=False,
            delivered_at=delivered_at,
            provider=provider,
            status_code=500,
            error_message=error_message,
            retry_count=retry_count,
            metadata=self._delivery_metadata(
                report=report,
            ),
        )

    @staticmethod
    def _delivery_metadata(
        *,
        report: ReportArtifact,
    ) -> dict[
        str,
        str,
    ]:
        return {
            "report_type": report.report_type,
            "artifact_type": str(
                report.artifact_type,
            ),
            "format": report.format or "",
            "content_type": report.content_type,
        }