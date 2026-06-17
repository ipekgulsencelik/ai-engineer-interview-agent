from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.evaluation.reporting.validators.bi_dataset_validator import (
    BIDatasetValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BIDataset:
    """
    Immutable BI dataset.

    Represents a business-intelligence-ready dataset
    generated from evaluation runs, telemetry metrics,
    report artifacts, dashboard widgets, experiments,
    model registry entries, and delivery outcomes.

    The full dataset should live in a storage backend.
    sample_rows is only for preview or inspection.
    """

    dataset_id: str

    dataset_name: str

    dataset_type: str

    source: str

    schema_version: str

    created_at: datetime

    row_count: int

    column_count: int

    storage_uri: str | None = None

    storage_backend: str | None = None

    tenant_id: str | None = None

    experiment_id: str | None = None

    run_id: str | None = None

    report_id: str | None = None

    benchmark_id: str | None = None

    owner: str | None = None

    description: str | None = None

    columns: tuple[
        str,
        ...,
    ] = ()

    primary_keys: tuple[
        str,
        ...,
    ] = ()

    partition_keys: tuple[
        str,
        ...,
    ] = ()

    sample_rows: tuple[
        dict[
            str,
            Any,
        ],
        ...,
    ] = ()

    tags: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        BIDatasetValidator.validate(
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_type=self.dataset_type,
            source=self.source,
            schema_version=self.schema_version,
            created_at=self.created_at,
            row_count=self.row_count,
            column_count=self.column_count,
            storage_uri=self.storage_uri,
            storage_backend=self.storage_backend,
            tenant_id=self.tenant_id,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            report_id=self.report_id,
            benchmark_id=self.benchmark_id,
            owner=self.owner,
            description=self.description,
            columns=self.columns,
            primary_keys=self.primary_keys,
            partition_keys=self.partition_keys,
            sample_rows=self.sample_rows,
            tags=self.tags,
            metadata=self.metadata,
        )

    @property
    def has_storage(
        self,
    ) -> bool:
        return (
            self.storage_uri is not None
            or self.storage_backend is not None
        )

    @property
    def has_tenant(
        self,
    ) -> bool:
        return (
            self.tenant_id
            is not None
        )

    @property
    def has_experiment(
        self,
    ) -> bool:
        return (
            self.experiment_id
            is not None
        )

    @property
    def has_run(
        self,
    ) -> bool:
        return (
            self.run_id
            is not None
        )

    @property
    def has_report(
        self,
    ) -> bool:
        return (
            self.report_id
            is not None
        )

    @property
    def has_benchmark(
        self,
    ) -> bool:
        return (
            self.benchmark_id
            is not None
        )

    @property
    def has_owner(
        self,
    ) -> bool:
        return (
            self.owner
            is not None
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_columns(
        self,
    ) -> bool:
        return bool(
            self.columns,
        )

    @property
    def has_primary_keys(
        self,
    ) -> bool:
        return bool(
            self.primary_keys,
        )

    @property
    def has_partition_keys(
        self,
    ) -> bool:
        return bool(
            self.partition_keys,
        )

    @property
    def has_sample_rows(
        self,
    ) -> bool:
        return bool(
            self.sample_rows,
        )

    @property
    def sample_row_count(
        self,
    ) -> int:
        return len(
            self.sample_rows,
        )

    @property
    def has_tags(
        self,
    ) -> bool:
        return bool(
            self.tags,
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return (
            self.row_count == 0
        )

    @property
    def is_wide(
        self,
    ) -> bool:
        return (
            self.column_count >= 50
        )

    @property
    def density_label(
        self,
    ) -> str:
        if self.row_count == 0:
            return "empty"

        if self.row_count < 1_000:
            return "small"

        if self.row_count < 1_000_000:
            return "medium"

        return "large"