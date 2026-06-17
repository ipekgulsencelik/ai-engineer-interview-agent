from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BI_DATASET_SCHEMA: Final[
    SchemaDefinition
] = {
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_name": NON_EMPTY_STRING_RULE,
    "dataset_type": NON_EMPTY_STRING_RULE,
    "source": NON_EMPTY_STRING_RULE,
    "schema_version": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "row_count": NON_NEGATIVE_NUMBER_RULE,
    "column_count": NON_NEGATIVE_NUMBER_RULE,
    "storage_uri": OPTIONAL_STRING_RULE,
    "storage_backend": OPTIONAL_STRING_RULE,
    "tenant_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "report_id": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "owner": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "columns": TUPLE_RULE,
    "primary_keys": TUPLE_RULE,
    "partition_keys": TUPLE_RULE,
    "sample_rows": TUPLE_RULE,
    "tags": TUPLE_RULE,
    "metadata": DICT_RULE,
}