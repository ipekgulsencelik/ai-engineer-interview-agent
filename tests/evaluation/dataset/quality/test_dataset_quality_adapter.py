"""Integration with the existing EvaluationDataset serialized samples."""

from __future__ import annotations

from src.domain.enums.level import Level
from src.evaluation.dataset.quality import (
    DatasetQualityEngine,
    EvaluationDatasetQualityAdapter,
    NonEmptyStringRule,
    RequiredFieldRule,
    UniqueFieldRule,
)
from src.evaluation.dataset.services.evaluation_dataset_assembly_service import (
    EvaluationDatasetAssemblyService,
)
from src.evaluation.domain.entities import EvaluationSample


def test_quality_adapter_reuses_existing_dataset_serialization() -> None:
    sample = EvaluationSample(
        sample_id="sample-1",
        question_id="question-1",
        question="What is RAG?",
        candidate_answer="Retrieval with generation.",
        expected_answer="Grounded generation.",
        category="RAG",
        level=Level.JR,
        retrieved_contexts=("evidence",),
        metadata={},
    )
    dataset = EvaluationDatasetAssemblyService.assemble(
        dataset_id="benchmark",
        dataset_name="Benchmark",
        dataset_version="1.2.0",
        description="Sample quality benchmark",
        samples=(sample,),
    )
    adapter = EvaluationDatasetQualityAdapter(
        engine=DatasetQualityEngine(
            record_rules=(
                RequiredFieldRule(
                    field_path="sample_id", rule_id="required-sample-id"
                ),
                NonEmptyStringRule(field_path="question", rule_id="question"),
            ),
            dataset_rules=(UniqueFieldRule(field_path="sample_id"),),
        )
    )
    result = adapter.evaluate(dataset=dataset)
    assert result.dataset_id == "benchmark"
    assert result.dataset_version == "1.2.0"
    assert result.record_count == 1
    assert result.total_checks == 3
    assert result.accepted
