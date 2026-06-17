from __future__ import annotations

from datetime import datetime
from typing import Any

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.bi_dataset_schema import (
    BI_DATASET_SCHEMA,
)


class BIDatasetValidator:
    """
    BIDataset validation service.
    """

    @staticmethod
    def validate(
        *,
        dataset_id: str,
        dataset_name: str,
        dataset_type: str,
        source: str,
        schema_version: str,
        created_at: datetime,
        row_count: int,
        column_count: int,
        storage_uri: str | None,
        storage_backend: str | None,
        tenant_id: str | None,
        experiment_id: str | None,
        run_id: str | None,
        report_id: str | None,
        benchmark_id: str | None,
        owner: str | None,
        description: str | None,
        columns: tuple[
            str,
            ...,
        ],
        primary_keys: tuple[
            str,
            ...,
        ],
        partition_keys: tuple[
            str,
            ...,
        ],
        sample_rows: tuple[
            dict[
                str,
                Any,
            ],
            ...,
        ],
        tags: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "dataset_type": dataset_type,
                "source": source,
                "schema_version": schema_version,
                "created_at": created_at,
                "row_count": row_count,
                "column_count": column_count,
                "storage_uri": storage_uri,
                "storage_backend": storage_backend,
                "tenant_id": tenant_id,
                "experiment_id": experiment_id,
                "run_id": run_id,
                "report_id": report_id,
                "benchmark_id": benchmark_id,
                "owner": owner,
                "description": description,
                "columns": columns,
                "primary_keys": primary_keys,
                "partition_keys": partition_keys,
                "sample_rows": sample_rows,
                "tags": tags,
                "metadata": metadata or {},
            },
            schema=BI_DATASET_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if column_count > 0 and len(columns) != column_count:
            raise EvaluationValidationError(
                "column_count must match columns length."
            )

        BIDatasetValidator._validate_unique_strings(
            values=columns,
            field_name="columns",
        )

        BIDatasetValidator._validate_unique_strings(
            values=primary_keys,
            field_name="primary_keys",
        )

        BIDatasetValidator._validate_unique_strings(
            values=partition_keys,
            field_name="partition_keys",
        )

        BIDatasetValidator._validate_unique_strings(
            values=tags,
            field_name="tags",
        )

        BIDatasetValidator._validate_subset(
            values=primary_keys,
            allowed_values=columns,
            field_name="primary_keys",
        )

        BIDatasetValidator._validate_subset(
            values=partition_keys,
            allowed_values=columns,
            field_name="partition_keys",
        )

        BIDatasetValidator._validate_sample_rows(
            sample_rows=sample_rows,
            columns=columns,
        )

        if metadata is not None:
            BIDatasetValidator._validate_string_dict(
                value=metadata,
                field_name="metadata",
            )

    @staticmethod
    def _validate_unique_strings(
        *,
        values: tuple[
            str,
            ...
        ],
        field_name: str,
    ) -> None:
        seen: set[
            str
        ] = set()

        for index, value in enumerate(values):
            if (
                not isinstance(value, str)
                or not value.strip()
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be a non-empty string."
                )

            if value in seen:
                raise EvaluationValidationError(
                    f"{field_name} values must be unique."
                )

            seen.add(value)

    @staticmethod
    def _validate_subset(
        *,
        values: tuple[
            str,
            ...
        ],
        allowed_values: tuple[
            str,
            ...
        ],
        field_name: str,
    ) -> None:
        allowed = set(allowed_values)

        for value in values:
            if value not in allowed:
                raise EvaluationValidationError(
                    f"{field_name} must be a subset of columns."
                )

    @staticmethod
    def _validate_sample_rows(
        *,
        sample_rows: tuple[
            dict[
                str,
                Any,
            ],
            ...
        ],
        columns: tuple[
            str,
            ...
        ],
    ) -> None:
        allowed_columns = set(columns)

        for row_index, row in enumerate(sample_rows):
            if not isinstance(row, dict):
                raise EvaluationValidationError(
                    f"sample_rows[{row_index}] must be a dictionary."
                )

            if columns and not set(row.keys()).issubset(allowed_columns):
                raise EvaluationValidationError(
                    f"sample_rows[{row_index}] contains unknown columns."
                )

    @staticmethod
    def _validate_string_dict(
        *,
        value: dict[
            str,
            str,
        ],
        field_name: str,
    ) -> None:
        for key, item in value.items():
            if (
                not isinstance(key, str)
                or not key.strip()
            ):
                raise EvaluationValidationError(
                    f"{field_name} keys must be non-empty strings."
                )

            if not isinstance(item, str):
                raise EvaluationValidationError(
                    f"{field_name} values must be strings."
                )