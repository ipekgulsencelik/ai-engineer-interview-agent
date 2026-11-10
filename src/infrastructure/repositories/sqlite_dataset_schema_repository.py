"""SQLite adapter for immutable versioned record schema definitions."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
    parse_schema_version,
)


def _decode_field(data: dict[str, Any]) -> DatasetField:
    nested = tuple(_decode_field(item) for item in data.get("properties", ()))
    item_data = data.get("items")
    return DatasetField(
        name=data["name"],
        kind=data["kind"],
        required=data.get("required", True),
        nullable=data.get("nullable", False),
        properties=nested,
        items=_decode_field(item_data) if item_data is not None else None,
    )


def _encode_schema(schema: DatasetRecordSchema) -> str:
    return json.dumps(asdict(schema), sort_keys=True, separators=(",", ":"))


class SQLiteDatasetSchemaRepository:
    """Persist immutable schema revisions; refuse version-content collisions."""

    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        with closing(sqlite3.connect(self._path)) as conn, conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS dataset_record_schemas (
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    definition_json TEXT NOT NULL,
                    PRIMARY KEY (name, version)
                )
                """
            )

    def register(self, *, schema: DatasetRecordSchema) -> None:
        definition = _encode_schema(schema)
        try:
            with closing(sqlite3.connect(self._path)) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                existing = conn.execute(
                    """
                    SELECT definition_json FROM dataset_record_schemas
                    WHERE name = ? AND version = ?
                    """,
                    (schema.name, schema.version),
                ).fetchone()
                if existing is not None:
                    if existing[0] != definition:
                        raise SchemaEvolutionError(
                            "schema version already registered with different content"
                        )
                    return
                conn.execute(
                    """
                    INSERT INTO dataset_record_schemas
                    (name, version, definition_json) VALUES (?, ?, ?)
                    """,
                    (schema.name, schema.version, definition),
                )
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("schema repository write failed") from exc

    def get_schema(
        self, *, name: str, version: str
    ) -> DatasetRecordSchema:
        parse_schema_version(version)
        try:
            with closing(sqlite3.connect(self._path)) as conn, conn:
                row = conn.execute(
                    """
                    SELECT definition_json FROM dataset_record_schemas
                    WHERE name = ? AND version = ?
                    """,
                    (name, version),
                ).fetchone()
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("schema repository read failed") from exc
        if row is None:
            raise SchemaEvolutionError(
                f"schema not registered: {name}@{version}"
            )
        try:
            data = json.loads(row[0])
            schema = DatasetRecordSchema(
                name=data["name"],
                version=data["version"],
                fields=tuple(_decode_field(item) for item in data["fields"]),
            )
        except (ValueError, TypeError, KeyError) as exc:
            raise SchemaEvolutionError("stored schema is invalid") from exc
        if schema.name != name or schema.version != version:
            raise SchemaEvolutionError("stored schema identity mismatch")
        return schema

    def list_versions(self, *, name: str) -> tuple[str, ...]:
        try:
            with closing(sqlite3.connect(self._path)) as conn, conn:
                rows = conn.execute(
                    "SELECT version FROM dataset_record_schemas WHERE name = ?",
                    (name,),
                ).fetchall()
        except sqlite3.DatabaseError as exc:
            raise SchemaEvolutionError("schema repository read failed") from exc
        return tuple(sorted((row[0] for row in rows), key=parse_schema_version))
