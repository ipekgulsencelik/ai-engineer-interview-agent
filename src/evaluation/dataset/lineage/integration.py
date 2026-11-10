"""Adapter between EvaluationDataset and content-addressed lineage nodes."""

from __future__ import annotations

from src.evaluation.dataset.entities.evaluation_dataset import EvaluationDataset
from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)


class EvaluationDatasetLineageAdapter:
    """Reference the existing dataset aggregate without serializing it again.

    The caller supplies the exact persisted artifact bytes; the lineage module
    hashes those bytes so provenance does not depend on lossy model projections.
    """

    @staticmethod
    def build_node(
        *,
        dataset: EvaluationDataset,
        artifact_bytes: bytes,
        producer: str,
        schema_version: str | None = None,
    ) -> DatasetLineageNode:
        return DatasetLineageNode.from_artifact(
            revision=DatasetRevision(
                dataset_id=dataset.dataset_id,
                version=dataset.dataset_version.version,
            ),
            content=artifact_bytes,
            producer=producer,
            created_at=dataset.metadata.created_at,
            schema_version=schema_version,
        )
