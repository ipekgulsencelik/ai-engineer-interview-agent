from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class ReportAttachmentResolver:
    """
    Resolves report artifact file path for delivery attachments.
    """

    def resolve(
        self,
        *,
        report: ReportArtifact,
    ) -> Path | None:
        path = Path(
            report.path,
        )

        if not path.exists():
            return None

        if not path.is_file():
            return None

        return path