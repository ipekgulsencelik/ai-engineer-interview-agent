from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)


class MLflowArtifactPathResolver:
    """
    Resolves report artifact local paths for MLflow delivery.
    """

    def resolve(
        self,
        *,
        report: ReportArtifact,
    ) -> Path:
        path = Path(
            report.path,
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Report artifact path does not exist: {path}",
            )

        if not path.is_file():
            raise ValueError(
                f"Report artifact path is not a file: {path}",
            )

        return path