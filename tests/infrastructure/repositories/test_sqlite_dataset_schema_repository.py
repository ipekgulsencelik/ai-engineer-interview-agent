"""Persistent schema registry contract and nested schema round-trip tests."""

from __future__ import annotations

import sqlite3

import pytest

from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    SchemaEvolutionError,
)
from src.infrastructure.repositories.sqlite_dataset_schema_repository import (
    SQLiteDatasetSchemaRepository,
)


def _schema(
    version: str = "1.0.0", *, field_name: str = "age"
) -> DatasetRecordSchema:
    return DatasetRecordSchema(
        name="interviews",
        version=version,
        fields=(
            DatasetField(
                "profile",
                "object",
                properties=(DatasetField(field_name, "integer"),),
            ),
            DatasetField(
                "reviews",
                "array",
                required=False,
                items=DatasetField(
                    "review",
                    "object",
                    properties=(
                        DatasetField("rating", "number"),
                        DatasetField("notes", "string", nullable=True),
                    ),
                ),
            ),
        ),
    )


def test_schema_registry_survives_restart_and_roundtrips_nested_schemas(
    tmp_path,
) -> None:
    location = tmp_path / "schemas.sqlite"
    repository = SQLiteDatasetSchemaRepository(location)
    schema = _schema()
    repository.register(schema=schema)

    reopened = SQLiteDatasetSchemaRepository(location)
    assert reopened.get_schema(name="interviews", version="1.0.0") == schema


def test_register_is_idempotent_but_rejects_immutable_version_collision(
    tmp_path,
) -> None:
    repository = SQLiteDatasetSchemaRepository(tmp_path / "schemas.sqlite")
    schema = _schema()
    repository.register(schema=schema)
    repository.register(schema=schema)
    with pytest.raises(SchemaEvolutionError, match="different content"):
        repository.register(schema=_schema(field_name="years"))
    assert repository.get_schema(
        name="interviews", version="1.0.0"
    ) == schema


def test_list_versions_returns_semver_order_not_lexicographic_order(
    tmp_path,
) -> None:
    repository = SQLiteDatasetSchemaRepository(tmp_path / "schemas.sqlite")
    for version in ("1.10.0", "2.0.0", "1.2.0"):
        repository.register(schema=_schema(version))
    assert repository.list_versions(name="interviews") == (
        "1.2.0",
        "1.10.0",
        "2.0.0",
    )


def test_registry_rejects_unknown_version(tmp_path) -> None:
    repository = SQLiteDatasetSchemaRepository(tmp_path / "schemas.sqlite")
    with pytest.raises(SchemaEvolutionError, match="not registered"):
        repository.get_schema(name="interviews", version="1.0.0")


def test_registry_rejects_corrupted_stored_schema(tmp_path) -> None:
    location = tmp_path / "schemas.sqlite"
    repository = SQLiteDatasetSchemaRepository(location)
    repository.register(schema=_schema())
    with sqlite3.connect(location) as conn:
        conn.execute(
            """
            UPDATE dataset_record_schemas SET definition_json = ?
            WHERE name = ? AND version = ?
            """,
            ('{"broken": true}', "interviews", "1.0.0"),
        )
    with pytest.raises(SchemaEvolutionError, match="stored schema is invalid"):
        repository.get_schema(name="interviews", version="1.0.0")
