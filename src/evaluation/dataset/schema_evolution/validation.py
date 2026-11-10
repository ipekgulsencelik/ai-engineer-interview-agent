"""Strict, recursive record validation with no implicit type coercion."""

from __future__ import annotations

import math
from collections.abc import Mapping

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
)


def _matches_kind(value: object, kind: str) -> bool:
    if kind == "string":
        return isinstance(value, str)
    if kind == "integer":
        return type(value) is int
    if kind == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    if kind == "boolean":
        return type(value) is bool
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    return False


class DatasetRecordValidator:
    """Validate nested objects/arrays using an explicit versioned schema."""

    def validate(
        self,
        *,
        schema: DatasetRecordSchema,
        record: Mapping[str, object],
    ) -> None:
        self._validate_fields(
            fields=schema.fields,
            record=record,
            prefix="",
        )

    def _validate_fields(
        self,
        *,
        fields: tuple[DatasetField, ...],
        record: Mapping[str, object],
        prefix: str,
    ) -> None:
        if not isinstance(record, Mapping):
            raise SchemaEvolutionError(f"{prefix or 'record'} must be a mapping")
        field_map = {field.name: field for field in fields}
        unknown = set(record) - set(field_map)
        if unknown:
            labels = sorted(str(key) for key in unknown)
            raise SchemaEvolutionError(
                f"unknown record fields at {prefix or 'root'}: {labels}"
            )
        for field in fields:
            path = f"{prefix}.{field.name}" if prefix else field.name
            if field.name not in record:
                if field.required:
                    raise SchemaEvolutionError(f"missing required field: {path}")
                continue
            self._validate_value(field=field, value=record[field.name], path=path)

    def _validate_value(
        self,
        *,
        field: DatasetField,
        value: object,
        path: str,
    ) -> None:
        if value is None:
            if not field.nullable:
                raise SchemaEvolutionError(f"field {path} cannot be null")
            return
        if not _matches_kind(value, field.kind):
            raise SchemaEvolutionError(
                f"field {path} must have kind {field.kind}"
            )
        if field.kind == "object" and field.properties:
            assert isinstance(value, dict)
            self._validate_fields(
                fields=field.properties,
                record=value,
                prefix=path,
            )
        if field.kind == "array" and field.items is not None:
            assert isinstance(value, list)
            for index, item in enumerate(value):
                self._validate_value(
                    field=field.items,
                    value=item,
                    path=f"{path}[{index}]",
                )
