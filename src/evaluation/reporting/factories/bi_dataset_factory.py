from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC
from datetime import datetime
from typing import Any
from uuid import uuid4

from src.evaluation.reporting.builders.bi_column_inference_builder import (
    BIColumnInferenceBuilder,
)
from src.evaluation.reporting.builders.bi_sample_row_builder import (
    BISampleRowBuilder,
)
from src.evaluation.reporting.entities.bi_dataset import (
    BIDataset,
)


class BIDatasetFactory:
    """
    Factory for creating BI dataset metadata entities.
    """

    def __init__(
        self,
        *,
        column_builder: BIColumnInferenceBuilder,
        sample_row_builder: BISampleRowBuilder,
    ) -> None:
        self._column_builder = column_builder
        self._sample_row_builder = sample_row_builder

    def create_pending(
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
        columns = self._column_builder.infer(
            rows=rows,
        )

        return BIDataset(
            dataset_id=str(
                uuid4(),
            ),
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            source=source,
            schema_version=schema_version,
            created_at=datetime.now(
                UTC,
            ),
            row_count=len(
                rows,
            ),
            column_count=len(
                columns,
            ),
            storage_uri=None,
            storage_backend=storage_backend,
            tenant_id=tenant_id,
            experiment_id=experiment_id,
            run_id=run_id,
            report_id=report_id,
            benchmark_id=benchmark_id,
            owner=owner,
            description=description,
            columns=columns,
            primary_keys=primary_keys,
            partition_keys=partition_keys,
            sample_rows=self._sample_row_builder.build(
                rows=rows,
            ),
            tags=tags,
            metadata=metadata,
        )

    def with_storage_uri(
        self,
        *,
        dataset: BIDataset,
        storage_uri: str,
    ) -> BIDataset:
        return BIDataset(
            dataset_id=dataset.dataset_id,
            dataset_name=dataset.dataset_name,
            dataset_type=dataset.dataset_type,
            source=dataset.source,
            schema_version=dataset.schema_version,
            created_at=dataset.created_at,
            row_count=dataset.row_count,
            column_count=dataset.column_count,
            storage_uri=storage_uri,
            storage_backend=dataset.storage_backend,
            tenant_id=dataset.tenant_id,
            experiment_id=dataset.experiment_id,
            run_id=dataset.run_id,
            report_id=dataset.report_id,
            benchmark_id=dataset.benchmark_id,
            owner=dataset.owner,
            description=dataset.description,
            columns=dataset.columns,
            primary_keys=dataset.primary_keys,
            partition_keys=dataset.partition_keys,
            sample_rows=dataset.sample_rows,
            tags=dataset.tags,
            metadata=dataset.metadata,
        )