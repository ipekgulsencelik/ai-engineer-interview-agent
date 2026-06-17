from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.mlflow_client import (
    MLflowClient,
)
from src.evaluation.reporting.services.mlflow_artifact_path_resolver import (
    MLflowArtifactPathResolver,
)
from src.evaluation.reporting.services.mlflow_delivery_result_factory import (
    MLflowDeliveryResultFactory,
)
from src.evaluation.reporting.services.mlflow_report_tag_logger import (
    MLflowReportTagLogger,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class MLflowReportDelivery:
    """
    Delivers report artifacts to MLflow Tracking.
    """

    def __init__(
        self,
        *,
        mlflow_client: MLflowClient,
        path_resolver: MLflowArtifactPathResolver,
        tag_logger: MLflowReportTagLogger,
        result_factory: MLflowDeliveryResultFactory,
        provider: str = "mlflow",
        artifact_path: str = "reports",
        log_metadata_tags: bool = True,
    ) -> None:
        self._mlflow_client = mlflow_client
        self._path_resolver = path_resolver
        self._tag_logger = tag_logger
        self._result_factory = result_factory
        self._provider = provider
        self._artifact_path = artifact_path
        self._log_metadata_tags = log_metadata_tags

    def deliver(
        self,
        *,
        report: ReportArtifact,
        run_id: str | None = None,
        artifact_path: str | None = None,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        delivered_at = datetime.now(
            UTC,
        )

        destination_run_id = (
            run_id
            or report.run_id
        )

        resolved_artifact_path = (
            artifact_path
            or self._artifact_path
        )

        try:
            if destination_run_id is None:
                raise ValueError(
                    "MLflow run_id is required for report delivery.",
                )

            local_path = self._path_resolver.resolve(
                report=report,
            )

            self._mlflow_client.log_artifact(
                run_id=destination_run_id,
                local_path=str(
                    local_path,
                ),
                artifact_path=resolved_artifact_path,
            )

            if self._log_metadata_tags:
                self._tag_logger.log(
                    report=report,
                    run_id=destination_run_id,
                )

            return self._result_factory.create_success(
                report=report,
                destination=destination_run_id,
                provider=self._provider,
                delivered_at=delivered_at,
                artifact_path=resolved_artifact_path,
                retry_count=retry_count,
            )

        except Exception as exc:
            return self._result_factory.create_failure(
                report=report,
                destination=destination_run_id or "unknown",
                provider=self._provider,
                delivered_at=delivered_at,
                artifact_path=resolved_artifact_path,
                error_message=str(
                    exc,
                ),
                retry_count=retry_count,
            )