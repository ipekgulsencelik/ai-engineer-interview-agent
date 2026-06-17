from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class WandbSummaryBuilder:
    """
    Builds W&B run summary payloads for report delivery.
    """

    def build(
        self,
        *,
        report: ReportArtifact,
    ) -> dict[
        str,
        object,
    ]:
        return {
            "evaluation_report_id": report.report_id,
            "evaluation_artifact_id": report.artifact_id,
            "evaluation_report_type": report.report_type,
            "evaluation_report_format": report.format or "",
            "evaluation_report_content_type": report.content_type,
        }