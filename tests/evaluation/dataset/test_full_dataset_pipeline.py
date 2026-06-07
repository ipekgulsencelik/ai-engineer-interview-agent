from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.evaluation.dataset.loaders.evaluation_sample_loader import (
    EvaluationSampleLoader,
)
from src.evaluation.dataset.loaders.human_annotation_loader import (
    HumanAnnotationLoader,
)
from src.evaluation.dataset.services.evaluation_dataset_assembly_service import (
    EvaluationDatasetAssemblyService,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _write_json(
    *,
    tmp_path: Path,
    file_name: str,
    payload: object,
) -> Path:
    file_path = tmp_path / file_name

    file_path.write_text(
        json.dumps(
            payload,
        ),
        encoding="utf-8",
    )

    return file_path


def test_full_dataset_pipeline_should_load_and_assemble_dataset(
    tmp_path: Path,
) -> None:
    samples_file = _write_json(
        tmp_path=tmp_path,
        file_name="evaluation_samples.json",
        payload=[
            {
                "sample_id": "sample-1",
                "question_id": "question-1",
                "question": "What is RAG?",
                "candidate_answer": (
                    "RAG combines retrieval and generation."
                ),
                "expected_answer": (
                    "Retrieval-Augmented Generation."
                ),
                "category": "RAG",
                "level": "JR",
                "retrieved_contexts": [
                    "RAG improves grounding.",
                ],
                "metadata": {
                    "source": "integration-test",
                },
            }
        ],
    )

    annotations_file = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=[
            {
                "sample_id": "sample-1",
                "evaluator_id": "evaluator-1",
                "overall_score": 85.0,
                "technical_score": 90.0,
                "communication_score": 80.0,
                "feedback": "Strong human evaluation.",
            }
        ],
    )

    samples = EvaluationSampleLoader().load(
        file_path=samples_file,
    )
    human_scores = HumanAnnotationLoader().load(
        file_path=annotations_file,
    )

    dataset = EvaluationDatasetAssemblyService.assemble(
        dataset_id="dataset-1",
        dataset_name="RAG Dataset",
        dataset_version="1.0.0",
        description="Full dataset pipeline integration test.",
        samples=samples,
        human_scores=human_scores,
        metadata={
            "source": "integration-test",
        },
    )

    assert dataset.dataset_id == "dataset-1"
    assert dataset.dataset_name == "RAG Dataset"
    assert dataset.dataset_version == "1.0.0"
    assert dataset.sample_ids == (
        "sample-1",
    )
    assert dataset.metadata["source"] == "integration-test"
    assert dataset.metadata["sample_count"] == 1
    assert dataset.metadata["human_score_count"] == 1
    assert dataset.metadata["llm_score_count"] == 0


def test_full_dataset_pipeline_should_raise_when_human_score_references_unknown_sample(
    tmp_path: Path,
) -> None:
    samples_file = _write_json(
        tmp_path=tmp_path,
        file_name="evaluation_samples.json",
        payload=[
            {
                "sample_id": "sample-1",
                "question_id": "question-1",
                "question": "What is RAG?",
                "candidate_answer": (
                    "RAG combines retrieval and generation."
                ),
                "expected_answer": (
                    "Retrieval-Augmented Generation."
                ),
                "category": "RAG",
                "level": "JR",
                "retrieved_contexts": [],
                "metadata": {},
            }
        ],
    )

    annotations_file = _write_json(
        tmp_path=tmp_path,
        file_name="human_annotations.json",
        payload=[
            {
                "sample_id": "missing-sample",
                "evaluator_id": "evaluator-1",
                "overall_score": 85.0,
                "technical_score": 90.0,
                "communication_score": 80.0,
                "feedback": "Valid feedback.",
            }
        ],
    )

    samples = EvaluationSampleLoader().load(
        file_path=samples_file,
    )
    human_scores = HumanAnnotationLoader().load(
        file_path=annotations_file,
    )

    with pytest.raises(
        EvaluationValidationError,
        match="HumanScore references unknown sample_id: missing-sample",
    ):
        EvaluationDatasetAssemblyService.assemble(
            dataset_id="dataset-1",
            dataset_name="RAG Dataset",
            dataset_version="1.0.0",
            description="Full dataset pipeline integration test.",
            samples=samples,
            human_scores=human_scores,
            metadata={},
        )