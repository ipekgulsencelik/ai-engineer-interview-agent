from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.evaluation.reporting.entities.bi_dataset import (
    BIDataset,
)
from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.reporting.factories.bi_dataset_factory import (
    BIDatasetFactory,
)
from src.evaluation.reporting.mappers.report_artifact_bi_row_mapper import (
    ReportArtifactBIRowMapper,
)
from src.evaluation.reporting.mappers.report_delivery_result_bi_row_mapper import (
    ReportDeliveryResultBIRowMapper,
)
from src.evaluation.reporting.mappers.telemetry_metric_bi_row_mapper import (
    TelemetryMetricBIRowMapper,
)
from src.evaluation.reporting.writers.bi_dataset_writer import (
    BIDatasetWriter,
)
from src.evaluation.reporting.entities.report_delivery_result import (
    ReportDeliveryResult,
)


class BIIntegrationService:
    """
    Service for exporting evaluation reporting data to BI.
    """

    def __init__(
        self,
        *,
        writer: BIDatasetWriter,
        dataset_factory: BIDatasetFactory,
        telemetry_mapper: TelemetryMetricBIRowMapper,
        report_mapper: ReportArtifactBIRowMapper,
        delivery_mapper: ReportDeliveryResultBIRowMapper,
    ) -> None:
        self._writer = writer
        self._dataset_factory = dataset_factory
        self._telemetry_mapper = telemetry_mapper
        self._report_mapper = report_mapper
        self._delivery_mapper = delivery_mapper

    def export_rows(
        self,
        *,
        dataset_name: str,
        dataset_type: str,
        source: str,
        rows: tuple[
            Mapping[
                str,
                Any,
            ],
            ...,
        ],
        schema_version: str = "1.0.0",
        storage_backend: str | None = None,
        tenant_id: str | None = None,
        experiment_id: str | None = None,
        run_id: str | None = None,
        report_id: str | None = None,
        benchmark_id: str | None = None,
        owner: str | None = None,
        description: str | None = None,
        primary_keys: tuple[
            str,
            ...,
        ] = (),
        partition_keys: tuple[
            str,
            ...,
        ] = (),
        tags: tuple[
            str,
            ...,
        ] = (),
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> BIDataset:
        dataset = self._dataset_factory.create_pending(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            source=source,
            rows=rows,
            schema_version=schema_version,
            storage_backend=storage_backend,
            tenant_id=tenant_id,
            experiment_id=experiment_id,
            run_id=run_id,
            report_id=report_id,
            benchmark_id=benchmark_id,
            owner=owner,
            description=description,
            primary_keys=primary_keys,
            partition_keys=partition_keys,
            tags=tags,
            metadata=metadata,
        )

        storage_uri = self._writer.write_dataset(
            dataset=dataset,
            rows=rows,
        )

        return self._dataset_factory.with_storage_uri(
            dataset=dataset,
            storage_uri=storage_uri,
        )

    def export_telemetry_metrics(
        self,
        *,
        metrics: tuple[
            TelemetryMetric,
            ...,
        ],
        dataset_name: str = "telemetry_metrics",
        schema_version: str = "1.0.0",
        storage_backend: str | None = None,
    ) -> BIDataset:
        rows = self._telemetry_mapper.to_rows(
            metrics=metrics,
        )

        return self.export_rows(
            dataset_name=dataset_name,
            dataset_type="telemetry_metrics",
            source="telemetry",
            rows=rows,
            schema_version=schema_version,
            storage_backend=storage_backend,
            tenant_id=self._first_value(
                values=tuple(
                    metric.tenant_id
                    for metric in metrics
                ),
            ),
            tags=(
                "telemetry",
                "metrics",
            ),
        )

    def export_report_artifacts(
        self,
        *,
        reports: tuple[
            ReportArtifact,
            ...,
        ],
        dataset_name: str = "report_artifacts",
        schema_version: str = "1.0.0",
        storage_backend: str | None = None,
    ) -> BIDataset:
        rows = self._report_mapper.to_rows(
            reports=reports,
        )

        return self.export_rows(
            dataset_name=dataset_name,
            dataset_type="report_artifacts",
            source="reporting",
            rows=rows,
            schema_version=schema_version,
            storage_backend=storage_backend,
            tags=(
                "reports",
                "artifacts",
            ),
        )

    def export_delivery_results(
        self,
        *,
        results: tuple[
            ReportDeliveryResult,
            ...,
        ],
        dataset_name: str = "report_delivery_results",
        schema_version: str = "1.0.0",
        storage_backend: str | None = None,
    ) -> BIDataset:
        rows = self._delivery_mapper.to_rows(
            results=results,
        )

        return self.export_rows(
            dataset_name=dataset_name,
            dataset_type="report_delivery_results",
            source="report_delivery",
            rows=rows,
            schema_version=schema_version,
            storage_backend=storage_backend,
            tags=(
                "reports",
                "delivery",
            ),
        )

    @staticmethod
    def _first_value(
        *,
        values: tuple[
            str | None,
            ...,
        ],
    ) -> str | None:
        for value in values:
            if value is not None:
                return value

        return None