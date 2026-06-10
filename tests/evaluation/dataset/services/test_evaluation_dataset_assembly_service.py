from __future__ import annotations

import pytest

from src.domain.enums.level import Level
from src.evaluation.dataset.services.evaluation_dataset_assembly_service import (
    EvaluationDatasetAssemblyService,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _sample(
    sample_id: str = "sample-1",
) -> EvaluationSample:
    return EvaluationSample(
        sample_id=sample_id,
        question_id="question-1",
        question="What is RAG?",
        candidate_answer="RAG combines retrieval and generation.",
        expected_answer="Retrieval-Augmented Generation.",
        category="RAG",
        level=Level.JR,
        retrieved_contexts=(
            "RAG improves grounding.",
        ),
        metadata={},
    )


def _human_score(
    sample_id: str = "sample-1",
) -> HumanScore:
    return HumanScore(
        sample_id=sample_id,
        evaluator_id="evaluator-1",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        feedback="Valid human feedback.",
    )


def _llm_score(
    sample_id: str = "sample-1",
) -> LLMScore:
    return LLMScore(
        sample_id=sample_id,
        model_name="gpt-5",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        reasoning_score=88.0,
        confidence_score=92.0,
        feedback="Valid LLM feedback.",
    )


def test_evaluation_dataset_assembly_service_should_create_dataset() -> None:
    dataset = EvaluationDatasetAssemblyService.assemble(
        dataset_id="dataset-1",
        dataset_name="RAG Dataset",
        dataset_version="1.0.0",
        description="Dataset for RAG evaluation.",
        samples=(
            _sample(),
        ),
        human_scores=(
            _human_score(),
        ),
        llm_scores=(
            _llm_score(),
        ),
        metadata={
            "source": "unit-test",
        },
    )

    assert dataset.dataset_id == "dataset-1"
    assert dataset.dataset_name == "RAG Dataset"
    assert dataset.dataset_version == "1.0.0"
    assert dataset.description == "Dataset for RAG evaluation."
    assert dataset.sample_ids == (
        "sample-1",
    )
    assert dataset.metadata["source"] == "unit-test"
    assert dataset.metadata["sample_count"] == 1
    assert dataset.metadata["human_score_count"] == 1
    assert dataset.metadata["llm_score_count"] == 1


def test_evaluation_dataset_assembly_service_should_raise_for_empty_samples() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="dataset must contain at least one sample",
    ):
        EvaluationDatasetAssemblyService.assemble(
            dataset_id="dataset-1",
            dataset_name="RAG Dataset",
            dataset_version="1.0.0",
            description="Dataset for RAG evaluation.",
            samples=(),
            human_scores=(),
            llm_scores=(),
            metadata={},
        )


def test_evaluation_dataset_assembly_service_should_raise_for_unknown_human_score_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="HumanScore references unknown sample_id: missing-sample",
    ):
        EvaluationDatasetAssemblyService.assemble(
            dataset_id="dataset-1",
            dataset_name="RAG Dataset",
            dataset_version="1.0.0",
            description="Dataset for RAG evaluation.",
            samples=(
                _sample("sample-1"),
            ),
            human_scores=(
                _human_score("missing-sample"),
            ),
            llm_scores=(),
            metadata={},
        )


def test_evaluation_dataset_assembly_service_should_raise_for_unknown_llm_score_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="LLMScore references unknown sample_id: missing-sample",
    ):
        EvaluationDatasetAssemblyService.assemble(
            dataset_id="dataset-1",
            dataset_name="RAG Dataset",
            dataset_version="1.0.0",
            description="Dataset for RAG evaluation.",
            samples=(
                _sample("sample-1"),
            ),
            human_scores=(),
            llm_scores=(
                _llm_score("missing-sample"),
            ),
            metadata={},
        )


def test_evaluation_dataset_assembly_service_should_preserve_sample_order() -> None:
    dataset = EvaluationDatasetAssemblyService.assemble(
        dataset_id="dataset-1",
        dataset_name="RAG Dataset",
        dataset_version="1.0.0",
        description="Dataset for RAG evaluation.",
        samples=(
            _sample("sample-1"),
            _sample("sample-2"),
            _sample("sample-3"),
        ),
        human_scores=(),
        llm_scores=(),
        metadata={},
    )

    assert dataset.sample_ids == (
        "sample-1",
        "sample-2",
        "sample-3",
    )