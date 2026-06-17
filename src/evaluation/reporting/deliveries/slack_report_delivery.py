from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.slack_client import (
    SlackClient,
)
from src.evaluation.reporting.services.slack_artifact_upload_service import (
    SlackArtifactUploadService,
)
from src.evaluation.reporting.factories.slack_delivery_result_factory import (
    SlackDeliveryResultFactory,
)
from src.evaluation.reporting.builders.slack_report_message_builder import (
    SlackReportMessageBuilder,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class SlackReportDelivery:
    """
    Delivers report artifacts to Slack channels.
    """

    def __init__(
        self,
        *,
        slack_client: SlackClient,
        message_builder: SlackReportMessageBuilder,
        upload_service: SlackArtifactUploadService,
        result_factory: SlackDeliveryResultFactory,
        provider: str = "slack",
    ) -> None:
        self._slack_client = slack_client
        self._message_builder = message_builder
        self._upload_service = upload_service
        self._result_factory = result_factory
        self._provider = provider

    def deliver(
        self,
        *,
        report: ReportArtifact,
        channel: str,
        message: str | None = None,
        upload_artifact: bool = True,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        delivered_at = datetime.now(
            UTC,
        )

        try:
            self._slack_client.post_message(
                channel=channel,
                message=self._message_builder.build(
                    report=report,
                    message=message,
                ),
            )

            self._upload_service.upload_if_requested(
                report=report,
                channel=channel,
                upload_artifact=upload_artifact,
            )

            return self._result_factory.create_success(
                report=report,
                channel=channel,
                provider=self._provider,
                delivered_at=delivered_at,
                retry_count=retry_count,
            )

        except Exception as exc:
            return self._result_factory.create_failure(
                report=report,
                channel=channel,
                provider=self._provider,
                delivered_at=delivered_at,
                error_message=str(
                    exc,
                ),
                retry_count=retry_count,
            )