"""Integration of immutable EvaluationDataset versions with artifact hashes."""

from __future__ import annotations

import hashlib

from src.domain.enums.level import Level
from src.evaluation.dataset.lineage import DatasetRevision
from src.evaluation.dataset.lineage.integration import (
    EvaluationDatasetLineageAdapter,
)
from src.evaluation.dataset.services.evaluation_dataset_assembly_service import (
    EvaluationDatasetAssemblyService,
)
from src.evaluation.domain.entities import EvaluationSample


def test_adapter_uses_real_dataset_identity_and_exact_artifact_bytes() -> None:
    sample = EvaluationSample(
        sample_id="sample-1",
        question_id="question-1",
        question="Define RAG",
        candidate_answer="Retrieval plus generation",
        expected_answer="Grounded generation",
        category="RAG",
        level=Level.JR,
        retrieved_contexts=("retrieved evidence",),
        metadata={},
    )
    dataset = EvaluationDatasetAssemblyService.assemble(
        dataset_id="benchmark-dataset",
        dataset_name="Interview benchmark",
        dataset_version="2.1.0",
        description="Interview candidate benchmark",
        samples=(sample,),
    )
    artifact = b'{"samples":[{"sample_id":"sample-1"}]}'
    node = EvaluationDatasetLineageAdapter.build_node(
        dataset=dataset,
        artifact_bytes=artifact,
        producer="benchmark-build",
        schema_version="1.0.0",
    )

    assert node.revision == DatasetRevision(
        dataset_id="benchmark-dataset", version="2.1.0"
    )
    assert node.content_sha256 == hashlib.sha256(artifact).hexdigest()
    assert node.created_at == dataset.metadata.created_at
    assert node.schema_version == "1.0.0"
