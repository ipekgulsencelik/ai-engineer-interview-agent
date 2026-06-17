from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.ports.wandb_client import (
    WandbClient,
)
from src.evaluation.reporting.builders.wandb_artifact_metadata_builder import (
    WandbArtifactMetadataBuilder,
)
from src.evaluation.reporting.resolvers.wandb_artifact_path_resolver import (
    WandbArtifactPathResolver,
)
from src.evaluation.reporting.factories.wandb_delivery_result_factory import (
    WandbDeliveryResultFactory,
)
from src.evaluation.reporting.builders.wandb_summary_builder import (
    WandbSummaryBuilder,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class WandbReportDelivery:
    """
    Delivers report artifacts to Weights & Biases.
    """

    def __init__(
        self,
        *,
        wandb_client: WandbClient,
        path_resolver: WandbArtifactPathResolver,
        metadata_builder: WandbArtifactMetadataBuilder,
        summary_builder: WandbSummaryBuilder,
        result_factory: WandbDeliveryResultFactory,
        provider: str = "wandb",
        log_summary: bool = True,
    ) -> None:
        self._wandb_client = wandb_client
        self._path_resolver = path_resolver
        self._metadata_builder = metadata_builder
        self._summary_builder = summary_builder
        self._result_factory = result_factory
        self._provider = provider
        self._log_summary = log_summary

    def deliver(
        self,
        *,
        report: ReportArtifact,
        run_id: str | None = None,
        artifact_name: str | None = None,
        retry_count: int = 0,
    ) -> ReportDeliveryResult:
        delivered_at = datetime.now(
            UTC,
        )

        destination_run_id = (
            run_id
            or report.run_id
        )

        try:
            if destination_run_id is None:
                raise ValueError(
                    "W&B run_id is required for report delivery.",
                )

            artifact_path = self._path_resolver.resolve(
                report=report,
            )

            self._wandb_client.log_artifact(
                run_id=destination_run_id,
                artifact_path=str(
                    artifact_path,
                ),
                artifact_name=self._metadata_builder.build_artifact_name(
                    report=report,
                    artifact_name=artifact_name,
                ),
                artifact_type=str(
                    report.artifact_type,
                ),
                metadata=self._metadata_builder.build_metadata(
                    report=report,
                ),
            )

            if self._log_summary:
                self._wandb_client.log_summary(
                    run_id=destination_run_id,
                    values=self._summary_builder.build(
                        report=report,
                    ),
                )

            return self._result_factory.create_success(
                report=report,
                destination=destination_run_id,
                provider=self._provider,
                delivered_at=delivered_at,
                retry_count=retry_count,
            )

        except Exception as exc:
            return self._result_factory.create_failure(
                report=report,
                destination=destination_run_id or "unknown",
                provider=self._provider,
                delivered_at=delivered_at,
                error_message=str(
                    exc,
                ),
                retry_count=retry_count,
            )