from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.domain.enums.level import Level
from src.evaluation.dataset.entities.dataset_metadata import (
    DatasetMetadata,
)
from src.evaluation.dataset.entities.dataset_version import (
    DatasetVersion,
)
from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _dataset_version() -> DatasetVersion:
    return DatasetVersion(
        version="1.0.0",
        stage=DatasetStage.DEVELOPMENT,
        created_by="system",
        description="Initial dataset version.",
    )


def _metadata() -> DatasetMetadata:
    return DatasetMetadata(
        created_at=datetime.now(timezone.utc),
        rubric_version="1.0.0",
        evaluator_version="1.0.0",
        source="unit-test",
        notes=None,
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
        retrieved_contexts=("RAG improves grounding.",),
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
        feedback="Valid feedback.",
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


def test_evaluation_dataset_should_create_successfully() -> None:
    dataset = EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=_dataset_version(),
        description="Evaluation dataset for RAG interview questions.",
        metadata=_metadata(),
        samples=(
            _sample("sample-1"),
            _sample("sample-2"),
        ),
        human_scores=(
            _human_score("sample-1"),
        ),
        llm_scores=(
            _llm_score("sample-2"),
        ),
    )

    assert dataset.dataset_id == "dataset-1"
    assert dataset.dataset_name == "RAG Benchmark Dataset"
    assert dataset.dataset_version.version == "1.0.0"
    assert dataset.description == (
        "Evaluation dataset for RAG interview questions."
    )
    assert dataset.sample_ids == (
        "sample-1",
        "sample-2",
    )
    assert dataset.sample_count == 2
    assert dataset.human_score_count == 1
    assert dataset.llm_score_count == 1


@pytest.mark.parametrize(
    "field_name",
    [
        "dataset_id",
        "dataset_name",
        "description",
    ],
)
def test_evaluation_dataset_should_raise_for_empty_string_fields(
    field_name: str,
) -> None:
    kwargs = {
        "dataset_id": "dataset-1",
        "dataset_name": "RAG Benchmark Dataset",
        "dataset_version": _dataset_version(),
        "description": "Evaluation dataset.",
        "metadata": _metadata(),
        "samples": (_sample(),),
        "human_scores": (),
        "llm_scores": (),
    }
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be empty",
    ):
        EvaluationDataset(**kwargs)


def test_evaluation_dataset_should_raise_for_invalid_dataset_version() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="dataset_version must be a DatasetVersion",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version="1.0.0",  # type: ignore[arg-type]
            description="Evaluation dataset.",
            metadata=_metadata(),
            samples=(_sample(),),
        )


def test_evaluation_dataset_should_raise_for_invalid_metadata() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="metadata must be a DatasetMetadata",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version=_dataset_version(),
            description="Evaluation dataset.",
            metadata={},  # type: ignore[arg-type]
            samples=(_sample(),),
        )


def test_evaluation_dataset_should_raise_for_empty_samples() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="dataset must contain at least one sample",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version=_dataset_version(),
            description="Evaluation dataset.",
            metadata=_metadata(),
            samples=(),
        )


def test_evaluation_dataset_should_raise_for_invalid_sample_item() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"samples\[0\] must be an EvaluationSample",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version=_dataset_version(),
            description="Evaluation dataset.",
            metadata=_metadata(),
            samples=("invalid",),  # type: ignore[arg-type]
        )


def test_evaluation_dataset_should_raise_for_unknown_human_score_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="HumanScore references unknown sample_id: missing-sample",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version=_dataset_version(),
            description="Evaluation dataset.",
            metadata=_metadata(),
            samples=(_sample("sample-1"),),
            human_scores=(_human_score("missing-sample"),),
        )


def test_evaluation_dataset_should_raise_for_unknown_llm_score_sample_id() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="LLMScore references unknown sample_id: missing-sample",
    ):
        EvaluationDataset(
            dataset_id="dataset-1",
            dataset_name="RAG Benchmark Dataset",
            dataset_version=_dataset_version(),
            description="Evaluation dataset.",
            metadata=_metadata(),
            samples=(_sample("sample-1"),),
            llm_scores=(_llm_score("missing-sample"),),
        )


def test_evaluation_dataset_should_be_immutable() -> None:
    dataset = EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=_dataset_version(),
        description="Evaluation dataset.",
        metadata=_metadata(),
        samples=(_sample(),),
    )

    with pytest.raises(
        AttributeError,
    ):
        dataset.dataset_id = "changed"  # type: ignore[misc]