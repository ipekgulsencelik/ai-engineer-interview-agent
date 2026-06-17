from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.evaluators.webhook_delivery_status_evaluator import (
    WebhookDeliveryStatusEvaluator,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class WebhookDeliveryResultFactory:
    """
    Factory for creating webhook delivery results.
    """

    DELIVERY_TYPE = "webhook"

    def __init__(
        self,
        *,
        status_evaluator: WebhookDeliveryStatusEvaluator,
    ) -> None:
        self._status_evaluator = status_evaluator

    def create_from_status(
        self,
        *,
        report: ReportArtifact,
        destination: str,
        provider: str,
        delivered_at: datetime,
        status_code: int | None,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        success = self._status_evaluator.is_success(
            status_code=status_code,
        )

        return ReportDeliveryResult(
            delivery_id=str(
                uuid4(),
            ),
            report_id=report.report_id,
            artifact_id=report.artifact_id,
            delivery_type=self.DELIVERY_TYPE,
            destination=destination,
            success=success,
            delivered_at=delivered_at,
            provider=provider,
            status_code=status_code,
            error_message=self._status_evaluator.error_message(
                status_code=status_code,
            ),
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
            "artifact_type": str(
                report.artifact_type,
            ),
            "format": report.format or "",
            "content_type": report.content_type,
        }