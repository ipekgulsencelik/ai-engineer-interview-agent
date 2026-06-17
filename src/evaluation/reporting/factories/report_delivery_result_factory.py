from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class ReportDeliveryResultFactory:
    """
    Factory for creating report delivery results.
    """

    def create_success(
        self,
        *,
        report: ReportArtifact,
        destination: str,
        delivery_type: str,
        provider: str,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=str(
                uuid4(),
            ),
            report_id=report.report_id,
            artifact_id=report.artifact_id,
            delivery_type=delivery_type,
            destination=destination,
            success=True,
            delivered_at=datetime.now(
                UTC,
            ),
            provider=provider,
            status_code=None,
            error_message=None,
            retry_count=retry_count,
            metadata=self._metadata(
                report=report,
            ),
        )

    def create_failure(
        self,
        *,
        report: ReportArtifact,
        destination: str,
        delivery_type: str,
        provider: str,
        error_message: str,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        return ReportDeliveryResult(
            delivery_id=str(
                uuid4(),
            ),
            report_id=report.report_id,
            artifact_id=report.artifact_id,
            delivery_type=delivery_type,
            destination=destination,
            success=False,
            delivered_at=datetime.now(
                UTC,
            ),
            provider=provider,
            status_code=None,
            error_message=error_message,
            retry_count=retry_count,
            metadata=self._metadata(
                report=report,
            ),
        )

    @staticmethod
    def _metadata(
        *,
        report: ReportArtifact,
    ) -> dict[
        str,
        str,
    ]:
        return {
            "report_type": report.report_type,
            "format": report.format or "",
            "content_type": report.content_type,
        }