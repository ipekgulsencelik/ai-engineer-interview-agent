from __future__ import annotations

from typing import Any

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class ReportArtifactBIRowMapper:
    """
    Maps report artifacts to BI rows.
    """

    def to_row(
        self,
        *,
        report: ReportArtifact,
    ) -> dict[
        str,
        Any,
    ]:
        return {
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
            "storage_backend": report.storage_backend,
            "format": report.format,
            "content_type": report.content_type,
            "size_bytes": report.size_bytes,
            "checksum": report.checksum,
            "generated_by": report.generated_by,
            "created_at": report.created_at.isoformat(),
            "description": report.description,
        }

    def to_rows(
        self,
        *,
        reports: tuple[
            ReportArtifact,
            ...,
        ],
    ) -> tuple[
        dict[
            str,
            Any,
        ],
        ...,
    ]:
        return tuple(
            self.to_row(
                report=report,
            )
            for report in reports
        )