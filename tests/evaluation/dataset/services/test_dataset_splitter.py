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
from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)
from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.dataset.services.dataset_splitter import (
    DatasetSplitter,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
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
    sample_id: str,
) -> EvaluationSample:
    return EvaluationSample(
        sample_id=sample_id,
        question_id=f"question-{sample_id}",
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


def _dataset(
    *,
    sample_count: int = 10,
) -> EvaluationDataset:
    return EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="RAG Benchmark Dataset",
        dataset_version=_dataset_version(),
        description="Evaluation dataset for RAG interview questions.",
        metadata=_metadata(),
        samples=tuple(
            _sample(
                sample_id=f"sample-{index}",
            )
            for index in range(
                1,
                sample_count + 1,
            )
        ),
    )


def test_dataset_splitter_should_create_train_validation_test_splits() -> None:
    train_split, validation_split, test_split = DatasetSplitter.split(
        dataset=_dataset(
            sample_count=10,
        ),
        train_ratio=0.70,
        validation_ratio=0.20,
        test_ratio=0.10,
        seed=42,
    )

    assert train_split.split_type is DatasetSplitType.TRAIN
    assert validation_split.split_type is DatasetSplitType.VALIDATION
    assert test_split.split_type is DatasetSplitType.TEST

    assert train_split.sample_count == 7
    assert validation_split.sample_count == 2
    assert test_split.sample_count == 1


def test_dataset_splitter_should_be_deterministic_for_same_seed() -> None:
    dataset = _dataset(
        sample_count=10,
    )

    first_result = DatasetSplitter.split(
        dataset=dataset,
        seed=42,
    )

    second_result = DatasetSplitter.split(
        dataset=dataset,
        seed=42,
    )

    assert first_result == second_result


def test_dataset_splitter_should_change_order_for_different_seed() -> None:
    dataset = _dataset(
        sample_count=10,
    )

    first_result = DatasetSplitter.split(
        dataset=dataset,
        seed=42,
    )

    second_result = DatasetSplitter.split(
        dataset=dataset,
        seed=99,
    )

    assert first_result != second_result


def test_dataset_splitter_should_not_drop_or_duplicate_samples() -> None:
    dataset = _dataset(
        sample_count=10,
    )

    train_split, validation_split, test_split = DatasetSplitter.split(
        dataset=dataset,
        seed=42,
    )

    split_sample_ids = (
        train_split.sample_ids
        + validation_split.sample_ids
        + test_split.sample_ids
    )

    assert set(split_sample_ids) == set(dataset.sample_ids)
    assert len(split_sample_ids) == len(set(split_sample_ids))
    assert len(split_sample_ids) == dataset.sample_count


def test_dataset_splitter_should_raise_for_invalid_ratio_sum() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="split ratios must sum to 1.0",
    ):
        DatasetSplitter.split(
            dataset=_dataset(
                sample_count=10,
            ),
            train_ratio=0.50,
            validation_ratio=0.30,
            test_ratio=0.30,
        )


@pytest.mark.parametrize(
    "train_ratio, validation_ratio, test_ratio",
    [
        (-0.1, 0.8, 0.3),
        (0.8, -0.1, 0.3),
        (0.8, 0.3, -0.1),
        (1.1, 0.0, -0.1),
    ],
)
def test_dataset_splitter_should_raise_for_ratio_out_of_range(
    train_ratio: float,
    validation_ratio: float,
    test_ratio: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="split ratios must be between 0 and 1",
    ):
        DatasetSplitter.split(
            dataset=_dataset(
                sample_count=10,
            ),
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
        )


def test_dataset_splitter_should_raise_for_small_dataset() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="dataset must contain at least 3 samples",
    ):
        DatasetSplitter.split(
            dataset=_dataset(
                sample_count=2,
            ),
        )