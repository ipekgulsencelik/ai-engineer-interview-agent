from __future__ import annotations

from src.evaluation.ops.entities.report_artifact import (
    ReportArtifact,
)


class WandbArtifactMetadataBuilder:
    """
    Builds W&B artifact metadata from report artifacts.
    """

    def build_artifact_name(
        self,
        *,
        report: ReportArtifact,
        artifact_name: str | None = None,
    ) -> str:
        if artifact_name is not None:
            return artifact_name

        return (
            "evaluation-report-"
            f"{report.report_id}"
        )

    def build_metadata(
        self,
        *,
        report: ReportArtifact,
    ) -> dict[
        str,
        object,
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
        }