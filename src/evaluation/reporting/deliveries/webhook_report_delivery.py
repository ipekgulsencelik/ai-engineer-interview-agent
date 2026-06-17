from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.webhook_client import (
    WebhookClient,
)
from src.evaluation.reporting.factories.webhook_delivery_result_factory import (
    WebhookDeliveryResultFactory,
)
from src.evaluation.reporting.builders.webhook_report_payload_builder import (
    WebhookReportPayloadBuilder,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class WebhookReportDelivery:
    """
    Delivers report artifact metadata through webhook.
    """

    def __init__(
        self,
        *,
        webhook_client: WebhookClient,
        payload_builder: WebhookReportPayloadBuilder,
        result_factory: WebhookDeliveryResultFactory,
        provider: str = "webhook",
    ) -> None:
        self._webhook_client = webhook_client
        self._payload_builder = payload_builder
        self._result_factory = result_factory
        self._provider = provider

    def deliver(
        self,
        *,
        report: ReportArtifact,
        url: str,
        headers: dict[str, str] | None = None,
        extra_payload: dict[str, object] | None = None,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        delivered_at = datetime.now(
            UTC,
        )

        try:
            status_code = self._webhook_client.post(
                url=url,
                payload=self._payload_builder.build(
                    report=report,
                    extra_payload=extra_payload,
                ),
                headers=headers,
            )

            return self._result_factory.create_from_status(
                report=report,
                destination=url,
                provider=self._provider,
                delivered_at=delivered_at,
                status_code=status_code,
                retry_count=retry_count,
            )

        except Exception as exc:
            return self._result_factory.create_failure(
                report=report,
                destination=url,
                provider=self._provider,
                delivered_at=delivered_at,
                error_message=str(
                    exc,
                ),
                retry_count=retry_count,
            )