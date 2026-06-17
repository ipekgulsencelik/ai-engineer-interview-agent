from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class EmailReportMessageBuilder:
    """
    Builds default email subject and body for report delivery.
    """

    def build_subject(
        self,
        *,
        report: ReportArtifact,
        subject: str | None = None,
    ) -> str:
        return subject or (
            "Evaluation Report: "
            f"{report.title}"
        )

    def build_body(
        self,
        *,
        report: ReportArtifact,
        body: str | None = None,
    ) -> str:
        return body or (
            "Hello,\n\n"
            "The requested evaluation report has been generated.\n\n"
            f"Report: {report.title}\n"
            f"Type: {report.report_type}\n"
            f"Format: {report.format or 'unknown'}\n\n"
            "Please see the attached report artifact.\n"
        )