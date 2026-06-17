from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class SlackReportMessageBuilder:
    """
    Builds Slack report delivery messages.
    """

    def build(
        self,
        *,
        report: ReportArtifact,
        message: str | None = None,
    ) -> str:
        if message is not None:
            return message

        return (
            "📊 Evaluation Report Available\n\n"
            f"Title: {report.title}\n"
            f"Type: {report.report_type}\n"
            f"Format: {report.format or 'unknown'}\n"
            f"Report ID: {report.report_id}\n"
        )