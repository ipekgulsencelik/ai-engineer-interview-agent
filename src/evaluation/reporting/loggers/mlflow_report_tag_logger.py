from __future__ import annotations

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.mlflow_client import (
    MLflowClient,
)


class MLflowReportTagLogger:
    """
    Logs report metadata as MLflow run tags.
    """

    def __init__(
        self,
        *,
        mlflow_client: MLflowClient,
    ) -> None:
        self._mlflow_client = mlflow_client

    def log(
        self,
        *,
        report: ReportArtifact,
        run_id: str,
    ) -> None:
        tags = {
            "evaluation.report_id": report.report_id,
            "evaluation.artifact_id": report.artifact_id,
            "evaluation.report_type": report.report_type,
            "evaluation.artifact_type": str(
                report.artifact_type,
            ),
            "evaluation.report_format": report.format or "",
            "evaluation.content_type": report.content_type,
        }

        for key, value in tags.items():
            self._mlflow_client.set_tag(
                run_id=run_id,
                key=key,
                value=value,
            )