from __future__ import annotations

from datetime import datetime, timezone

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
from src.evaluation.dataset.services.dataset_hash_generator import (
    DatasetHashGenerator,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
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
        created_at=datetime(
            2026,
            6,
            7,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        ),
        rubric_version="1.0.0",
        evaluator_version="1.0.0",
        source="unit-test",
        notes=None,
    )


def _sample(
    *,
    sample_id: str = "sample-1",
    question_id: str = "question-1",
    question: str = "What is RAG?",
    candidate_answer: str = "RAG combines retrieval and generation.",
    expected_answer: str = "Retrieval-Augmented Generation.",
    category: str = "RAG",
    level: Level = Level.JR,
) -> EvaluationSample:
    return EvaluationSample(
        sample_id=sample_id,
        question_id=question_id,
        question=question,
        candidate_answer=candidate_answer,
        expected_answer=expected_answer,
        category=category,
        level=level,
        retrieved_contexts=(
            "RAG improves grounding.",
        ),
        metadata={},
    )


def _human_score(
    *,
    sample_id: str = "sample-1",
    evaluator_id: str = "evaluator-1",
    overall_score: float = 85.0,
    technical_score: float = 90.0,
    communication_score: float = 80.0,
) -> HumanScore:
    return HumanScore(
        sample_id=sample_id,
        evaluator_id=evaluator_id,
        overall_score=overall_score,
        technical_score=technical_score,
        communication_score=communication_score,
        feedback="Valid human feedback.",
    )


def _llm_score(
    *,
    sample_id: str = "sample-1",
    model_name: str = "gpt-5",
    overall_score: float = 85.0,
    technical_score: float = 90.0,
    communication_score: float = 80.0,
    reasoning_score: float = 88.0,
    confidence_score: float = 92.0,
) -> LLMScore:
    return LLMScore(
        sample_id=sample_id,
        model_name=model_name,
        overall_score=overall_score,
        technical_score=technical_score,
        communication_score=communication_score,
        reasoning_score=reasoning_score,
        confidence_score=confidence_score,
        feedback="Valid LLM feedback.",
    )


def _dataset(
    *,
    samples: tuple[EvaluationSample, ...] | None = None,
    human_scores: tuple[HumanScore, ...] | None = None,
    llm_scores: tuple[LLMScore, ...] | None = None,
) -> EvaluationDataset:
    return EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=_dataset_version(),
        description="Evaluation dataset for RAG interview questions.",
        metadata=_metadata(),
        samples=samples
        or (
            _sample(),
        ),
        human_scores=human_scores
        or (
            _human_score(),
        ),
        llm_scores=llm_scores
        or (
            _llm_score(),
        ),
    )


def test_dataset_hash_generator_should_generate_hash() -> None:
    dataset_hash = DatasetHashGenerator().generate(
        dataset=_dataset(),
    )

    assert isinstance(
        dataset_hash,
        str,
    )
    assert len(dataset_hash) == 64


def test_dataset_hash_generator_should_be_deterministic() -> None:
    generator = DatasetHashGenerator()
    dataset = _dataset()

    first_hash = generator.generate(
        dataset=dataset,
    )
    second_hash = generator.generate(
        dataset=dataset,
    )

    assert first_hash == second_hash


def test_dataset_hash_generator_should_change_when_sample_changes() -> None:
    generator = DatasetHashGenerator()

    first_hash = generator.generate(
        dataset=_dataset(
            samples=(
                _sample(
                    sample_id="sample-1",
                    question="What is RAG?",
                ),
            ),
            human_scores=(
                _human_score(
                    sample_id="sample-1",
                ),
            ),
            llm_scores=(
                _llm_score(
                    sample_id="sample-1",
                ),
            ),
        ),
    )

    second_hash = generator.generate(
        dataset=_dataset(
            samples=(
                _sample(
                    sample_id="sample-1",
                    question="What is vector search?",
                ),
            ),
            human_scores=(
                _human_score(
                    sample_id="sample-1",
                ),
            ),
            llm_scores=(
                _llm_score(
                    sample_id="sample-1",
                ),
            ),
        ),
    )

    assert first_hash != second_hash


def test_dataset_hash_generator_should_change_when_human_score_changes() -> None:
    generator = DatasetHashGenerator()

    first_hash = generator.generate(
        dataset=_dataset(
            human_scores=(
                _human_score(
                    overall_score=85.0,
                ),
            ),
        ),
    )

    second_hash = generator.generate(
        dataset=_dataset(
            human_scores=(
                _human_score(
                    overall_score=90.0,
                ),
            ),
        ),
    )

    assert first_hash != second_hash


def test_dataset_hash_generator_should_change_when_llm_score_changes() -> None:
    generator = DatasetHashGenerator()

    first_hash = generator.generate(
        dataset=_dataset(
            llm_scores=(
                _llm_score(
                    reasoning_score=88.0,
                ),
            ),
        ),
    )

    second_hash = generator.generate(
        dataset=_dataset(
            llm_scores=(
                _llm_score(
                    reasoning_score=95.0,
                ),
            ),
        ),
    )

    assert first_hash != second_hash


def test_dataset_hash_generator_should_change_when_version_changes() -> None:
    dataset_v1 = EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=_dataset_version(),
        description="Evaluation dataset for RAG interview questions.",
        metadata=_metadata(),
        samples=(
            _sample(),
        ),
        human_scores=(
            _human_score(),
        ),
        llm_scores=(
            _llm_score(),
        ),
    )

    dataset_v2 = EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=DatasetVersion(
            version="1.0.1",
            stage=DatasetStage.DEVELOPMENT,
            created_by="system",
            description="Patch dataset version.",
        ),
        description="Evaluation dataset for RAG interview questions.",
        metadata=_metadata(),
        samples=(
            _sample(),
        ),
        human_scores=(
            _human_score(),
        ),
        llm_scores=(
            _llm_score(),
        ),
    )

    assert DatasetHashGenerator().generate(
        dataset=dataset_v1,
    ) != DatasetHashGenerator().generate(
        dataset=dataset_v2,
    )