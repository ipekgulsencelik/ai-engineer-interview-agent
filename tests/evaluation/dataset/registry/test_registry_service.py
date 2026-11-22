"""SOLID contracts: publish only immutable, registered lineage revisions."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry import (
    DatasetCatalogEntry,
    DatasetRegistryError,
    DatasetRegistryLineageError,
    DatasetRegistryService,
)
from src.infrastructure.repositories.sqlite_dataset_lineage_repository import (
    SQLiteDatasetLineageRepository,
)
from src.infrastructure.repositories.sqlite_dataset_registry_repository import (
    SQLiteDatasetRegistryRepository,
)


def _node(
    version: str = "1.0.0", *, content: bytes = b"exact-published-artifact"
) -> DatasetLineageNode:
    return DatasetLineageNode.from_artifact(
        revision=DatasetRevision(dataset_id="interview-qa", version=version),
        content=content,
        producer="evaluation-pipeline",
        created_at=datetime(2026, 11, 23, tzinfo=UTC),
        schema_version="1.0.0",
    )


def test_end_to_end_lineage_backed_registration_and_idempotency(tmp_path) -> None:
    lineage = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    registry = SQLiteDatasetRegistryRepository(tmp_path / "catalog.sqlite")
    node = _node()
    lineage.register(node=node, parents=())
    service = DatasetRegistryService(lineage=lineage, registry=registry)

    published = service.register(
        node=node,
        name="Evaluation Q&A",
        owner_id="evaluation-team",
        tags=("training", "curated"),
        description="No raw samples in the registry.",
    )
    assert published.created
    assert published.entry.tags == ("curated", "training")
    assert not service.register(
        node=node,
        name="Evaluation Q&A",
        owner_id="evaluation-team",
        tags=("curated", "training"),
        description="No raw samples in the registry.",
    ).created
    assert service.get(revision=node.revision) == published.entry
    assert service.list_versions(dataset_id="interview-qa") == (published.entry,)
    assert service.list_by_tag(tag="curated") == (published.entry,)

    reloaded = SQLiteDatasetRegistryRepository(tmp_path / "catalog.sqlite")
    assert reloaded.get(revision=node.revision) == published.entry


def test_lineage_missing_or_content_mismatch_is_rejected(tmp_path) -> None:
    lineage = SQLiteDatasetLineageRepository(tmp_path / "lineage.sqlite")
    registry = SQLiteDatasetRegistryRepository(tmp_path / "registry.sqlite")
    service = DatasetRegistryService(lineage=lineage, registry=registry)
    node = _node()

    with pytest.raises(DatasetRegistryLineageError, match="lineage"):
        service.register(node=node, name="Dataset", owner_id="team")
    lineage.register(node=node, parents=())

    forged = _node(content=b"tampered-artifact")
    with pytest.raises(DatasetRegistryLineageError, match="lineage"):
        service.register(node=forged, name="Dataset", owner_id="team")

    assert registry.get(revision=node.revision) is None


@pytest.mark.parametrize(
    ("changes", "match"),
    [
        ({"name": ""}, "name"),
        ({"owner_id": " "}, "owner_id"),
        ({"producer": ""}, "producer"),
        ({"content_sha256": "bad"}, "content_sha256"),
        ({"created_at": datetime(2026, 11, 23)}, "timezone-aware"),
        ({"tags": ("Private",)}, "tags"),
        ({"tags": ("valid", "valid")}, "tags"),
        ({"tags": tuple(f"t{i}" for i in range(33))}, "tags"),
        ({"description": "x" * 513}, "description"),
        ({"schema_version": "v1"}, "MAJOR.MINOR.PATCH"),
    ],
)
def test_catalog_rejects_invalid_metadata(changes: dict, match: str) -> None:
    entry = DatasetCatalogEntry.from_lineage(
        node=_node(), name="Evaluation Q&A", owner_id="team"
    )
    with pytest.raises(ValueError, match=match):
        replace(entry, **changes)


def test_catalog_requires_real_lineage_node_and_revision() -> None:
    with pytest.raises(DatasetRegistryError, match="node"):
        DatasetCatalogEntry.from_lineage(
            node=None, name="Dataset", owner_id="team"  # type: ignore[arg-type]
        )
    with pytest.raises(DatasetRegistryError, match="revision"):
        replace(
            DatasetCatalogEntry.from_lineage(
                node=_node(), name="Dataset", owner_id="team"
            ),
            revision="wrong",  # type: ignore[arg-type]
        )


def test_catalog_entry_does_not_embed_sensitive_source_artifact() -> None:
    node = _node(content=b"PERSONAL-ANSWER-DO-NOT-STORE")
    entry = DatasetCatalogEntry.from_lineage(
        node=node, name="Dataset", owner_id="team"
    )
    assert not hasattr(entry, "content")
    assert not hasattr(entry, "records")
    assert entry.content_sha256 == node.content_sha256
