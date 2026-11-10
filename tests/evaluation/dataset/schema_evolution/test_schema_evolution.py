"""Behavioral tests for versioned schemas and explicit record migrations."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy

import pytest

from src.evaluation.dataset.schema_evolution import (
    DatasetField,
    DatasetRecordSchema,
    DatasetRecordValidator,
    DropField,
    MigrationRegistry,
    MigrationStep,
    RenameField,
    SchemaCompatibilityChecker,
    SchemaEvolutionError,
    SchemaEvolutionService,
    SetDefault,
)


def _schema(
    version: str = "1.0.0",
    *,
    fields: tuple[DatasetField, ...] | None = None,
    name: str = "samples",
) -> DatasetRecordSchema:
    return DatasetRecordSchema(
        name=name,
        version=version,
        fields=fields if fields is not None else (DatasetField("id", "string"),),
    )


@pytest.mark.parametrize("version", ["1", "v1.0.0", "1.0", "01.0.0", "1.0.0-rc1"])
def test_schema_rejects_invalid_versions(version: str) -> None:
    with pytest.raises(SchemaEvolutionError, match="MAJOR.MINOR.PATCH"):
        _schema(version)


def test_schema_requires_unique_immutable_fields() -> None:
    with pytest.raises(SchemaEvolutionError, match="duplicate"):
        _schema(fields=(DatasetField("id", "string"), DatasetField("id", "number")))
    with pytest.raises(SchemaEvolutionError, match="tuple"):
        _schema(fields=[])  # type: ignore[arg-type]


def test_schema_rejects_unsupported_field_kind() -> None:
    with pytest.raises(SchemaEvolutionError, match="unsupported"):
        DatasetField("name", "date")


@pytest.mark.parametrize(
    "record,match",
    [
        ({}, "missing required"),
        ({"id": "s1", "extra": 10}, "unknown record fields"),
        ({"id": None}, "cannot be null"),
        ({"id": 1}, "kind string"),
    ],
)
def test_validator_rejects_invalid_records(
    record: dict[str, object], match: str
) -> None:
    with pytest.raises(SchemaEvolutionError, match=match):
        DatasetRecordValidator().validate(schema=_schema(), record=record)


def test_validator_handles_optional_nullable_fields() -> None:
    schema = _schema(
        fields=(
            DatasetField("id", "string"),
            DatasetField("comment", "string", required=False, nullable=True),
        )
    )
    validator = DatasetRecordValidator()
    validator.validate(schema=schema, record={"id": "s1"})
    validator.validate(schema=schema, record={"id": "s1", "comment": None})
    validator.validate(schema=schema, record={"id": "s1", "comment": "ok"})


@pytest.mark.parametrize("value", [True, False, 1.4, "1"])
def test_integer_validation_rejects_non_integer_values(value: object) -> None:
    schema = _schema(fields=(DatasetField("score", "integer"),))
    with pytest.raises(SchemaEvolutionError, match="kind integer"):
        DatasetRecordValidator().validate(schema=schema, record={"score": value})


@pytest.mark.parametrize("value", [True, float("inf"), float("nan")])
def test_numeric_validation_rejects_booleans_and_nonfinite(
    value: object,
) -> None:
    schema = _schema(fields=(DatasetField("score", "number"),))
    with pytest.raises(SchemaEvolutionError, match="kind number"):
        DatasetRecordValidator().validate(schema=schema, record={"score": value})


def test_compatibility_accepts_optional_addition_and_relaxation() -> None:
    old = _schema(fields=(DatasetField("id", "string"),))
    new = _schema(
        "1.1.0",
        fields=(
            DatasetField("id", "string", required=False, nullable=True),
            DatasetField("notes", "string", required=False),
        ),
    )
    report = SchemaCompatibilityChecker().compare(source=old, target=new)
    assert report.backward_compatible
    assert report.breaking_changes == ()
    assert "new optional field: notes" in report.safe_changes


@pytest.mark.parametrize(
    "target_fields,expected",
    [
        ((DatasetField("id", "string"), DatasetField("x", "string")), "new required"),
        ((DatasetField("other", "string"),), "removed field"),
        ((DatasetField("id", "number"),), "changed type"),
    ],
)
def test_compatibility_identifies_breaking_changes(
    target_fields: tuple[DatasetField, ...], expected: str
) -> None:
    report = SchemaCompatibilityChecker().compare(
        source=_schema(),
        target=_schema("2.0.0", fields=target_fields),
    )
    assert not report.backward_compatible
    assert any(expected in change for change in report.breaking_changes)


def test_compatibility_detects_tightened_constraints() -> None:
    old = _schema(
        fields=(DatasetField("id", "string", required=False, nullable=True),)
    )
    new = _schema("1.1.0", fields=(DatasetField("id", "string"),))
    report = SchemaCompatibilityChecker().compare(source=old, target=new)
    assert len(report.breaking_changes) == 2


def test_same_version_cannot_have_different_schema() -> None:
    with pytest.raises(SchemaEvolutionError, match="version bump"):
        SchemaCompatibilityChecker().compare(
            source=_schema(),
            target=_schema(fields=(DatasetField("other", "string"),)),
        )


def test_compatibility_rejects_mismatched_schema_names() -> None:
    with pytest.raises(SchemaEvolutionError, match="different schema"):
        SchemaCompatibilityChecker().compare(
            source=_schema(),
            target=_schema("2.0.0", name="other"),
        )


def test_migration_chains_rename_drop_and_default_without_mutating() -> None:
    v1 = _schema(
        fields=(
            DatasetField("id", "string"),
            DatasetField("response", "string"),
            DatasetField("legacy", "boolean"),
        )
    )
    v3 = _schema(
        "3.0.0",
        fields=(
            DatasetField("id", "string"),
            DatasetField("answer", "string"),
            DatasetField("status", "string"),
            DatasetField("tags", "array"),
        ),
    )
    registry = MigrationRegistry(
        (
            MigrationStep(
                "1.0.0",
                "2.0.0",
                (
                    RenameField("response", "answer"),
                    DropField("legacy"),
                    SetDefault("status", "ready"),
                ),
            ),
            MigrationStep("2.0.0", "3.0.0", (SetDefault("tags", []),)),
        )
    )
    records = [
        {"id": "a", "response": "A", "legacy": True},
        {"id": "b", "response": "B", "legacy": False},
    ]
    original = deepcopy(records)

    result = SchemaEvolutionService(migrations=registry).migrate_records(
        records=records, source_schema=v1, target_schema=v3
    )

    assert result == (
        {"id": "a", "answer": "A", "status": "ready", "tags": []},
        {"id": "b", "answer": "B", "status": "ready", "tags": []},
    )
    assert records == original
    assert result[0]["tags"] is not result[1]["tags"]


def test_failed_batch_keeps_inputs_unchanged() -> None:
    source = _schema()
    target = _schema(
        "1.1.0", fields=(DatasetField("id", "string"), DatasetField("x", "integer"))
    )
    service = SchemaEvolutionService(
        migrations=MigrationRegistry(
            [MigrationStep("1.0.0", "1.1.0", (SetDefault("x", 1),))]
        )
    )
    records = [{"id": "ok"}, {"id": 123}]
    before = deepcopy(records)
    with pytest.raises(SchemaEvolutionError, match=r"record\[1\]"):
        service.migrate_records(
            records=records, source_schema=source, target_schema=target
        )
    assert records == before


def test_rename_rejects_collision_instead_of_overwriting() -> None:
    with pytest.raises(SchemaEvolutionError, match="overwrite"):
        RenameField("old", "new").apply({"old": 1, "new": 2})


def test_migration_registry_rejects_duplicate_origins() -> None:
    with pytest.raises(SchemaEvolutionError, match="duplicate migration"):
        MigrationRegistry(
            [
                MigrationStep("1.0.0", "1.1.0", ()),
                MigrationStep("1.0.0", "2.0.0", ()),
            ]
        )


def test_migration_registry_rejects_downgrades_and_missing_paths() -> None:
    registry = MigrationRegistry([MigrationStep("1.0.0", "1.1.0", ())])
    with pytest.raises(SchemaEvolutionError, match="downgrade"):
        registry.resolve(source_version="1.1.0", target_version="1.0.0")
    with pytest.raises(SchemaEvolutionError, match="missing migration"):
        registry.resolve(source_version="1.0.0", target_version="2.0.0")
    with pytest.raises(SchemaEvolutionError, match="greater"):
        MigrationStep("2.0.0", "1.0.0", ())


def test_service_requires_explicit_version_step_for_compatible_change() -> None:
    with pytest.raises(SchemaEvolutionError, match="missing migration"):
        SchemaEvolutionService(migrations=MigrationRegistry()).migrate_records(
            records=[{"id": "x"}],
            source_schema=_schema(),
            target_schema=_schema(
                "1.1.0",
                fields=(
                    DatasetField("id", "string"),
                    DatasetField("notes", "string", required=False),
                ),
            ),
        )


def test_identity_migration_validates_and_copies() -> None:
    record = {"id": "x"}
    result = SchemaEvolutionService(
        migrations=MigrationRegistry()
    ).migrate_records(
        records=[record], source_schema=_schema(), target_schema=_schema()
    )
    assert result == ({"id": "x"},)
    assert result[0] is not record


class _CustomOperation:
    def apply(self, record: Mapping[str, object]) -> dict[str, object]:
        return {**record, "label": "evaluated"}


def test_custom_operation_supports_extension_without_service_changes() -> None:
    target = _schema(
        "1.1.0",
        fields=(
            DatasetField("id", "string"),
            DatasetField("label", "string"),
        ),
    )
    step = MigrationStep("1.0.0", "1.1.0", (_CustomOperation(),))
    result = SchemaEvolutionService(
        migrations=MigrationRegistry([step])
    ).migrate_records(
        records=[{"id": "x"}],
        source_schema=_schema(),
        target_schema=target,
    )
    assert result == ({"id": "x", "label": "evaluated"},)
