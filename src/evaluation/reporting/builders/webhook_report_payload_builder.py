from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class WebhookReportPayloadBuilder:
    """
    Builds webhook payloads for report artifact delivery.
    """

    EVENT_TYPE = "evaluation.report.generated"

    def build(
        self,
        *,
        report: ReportArtifact,
        extra_payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "event_type": self.EVENT_TYPE,
            "report": {
                "report_id": report.report_id,
                "artifact_id": report.artifact_id,
                "run_id": report.run_id,
                "experiment_id": report.experiment_id,
                "title": report.title,
                "report_type": report.report_type,
                "artifact_type": str(
                    report.artifact_type,
                ),
                "path": report.path,
                "uri": report.uri,
                "format": report.format,
                "content_type": report.content_type,
                "size_bytes": report.size_bytes,
                "checksum": report.checksum,
                "generated_by": report.generated_by,
                "created_at": report.created_at.isoformat(),
                "description": report.description,
                "tags": list(
                    report.tags,
                )
                if report.tags is not None
                else [],
                "metadata": report.metadata or {},
            },
        }

        if extra_payload is not None:
            payload["extra"] = extra_payload

        return payload