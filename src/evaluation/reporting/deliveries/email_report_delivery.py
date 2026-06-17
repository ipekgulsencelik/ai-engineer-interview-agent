from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.email_sender import (
    EmailSender,
)
from src.evaluation.reporting.services.email_report_message_builder import (
    EmailReportMessageBuilder,
)
from src.evaluation.reporting.resolvers.report_attachment_resolver import (
    ReportAttachmentResolver,
)
from src.evaluation.reporting.factories.report_delivery_result_factory import (
    ReportDeliveryResultFactory,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class EmailReportDelivery:
    """
    Delivers report artifacts through email.
    """

    DELIVERY_TYPE = "email"

    def __init__(
        self,
        *,
        sender: EmailSender,
        message_builder: EmailReportMessageBuilder,
        attachment_resolver: ReportAttachmentResolver,
        result_factory: ReportDeliveryResultFactory,
        provider: str = "email",
    ) -> None:
        self._sender = sender
        self._message_builder = message_builder
        self._attachment_resolver = attachment_resolver
        self._result_factory = result_factory
        self._provider = provider

    def deliver(
        self,
        *,
        report: ReportArtifact,
        recipient: str,
        subject: str | None = None,
        body: str | None = None,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        try:
            self._sender.send(
                to=recipient,
                subject=self._message_builder.build_subject(
                    report=report,
                    subject=subject,
                ),
                body=self._message_builder.build_body(
                    report=report,
                    body=body,
                ),
                attachment_path=self._attachment_resolver.resolve(
                    report=report,
                ),
            )

            return self._result_factory.create_success(
                report=report,
                destination=recipient,
                delivery_type=self.DELIVERY_TYPE,
                provider=self._provider,
                retry_count=retry_count,
            )

        except Exception as exc:
            return self._result_factory.create_failure(
                report=report,
                destination=recipient,
                delivery_type=self.DELIVERY_TYPE,
                provider=self._provider,
                error_message=str(
                    exc,
                ),
                retry_count=retry_count,
            )