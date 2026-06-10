from __future__ import annotations

from datetime import datetime

import pytest

from src.domain.enums.level import (
    Level,
)
from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.dataset.entities.dataset_metadata import (
    DatasetMetadata,
)
from src.evaluation.dataset.value_objects.dataset_split import (
    DatasetSplit,
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
from src.evaluation.dataset.services.dataset_distribution_analyzer import (
    DatasetDistributionAnalyzer,
)
from src.evaluation.domain.entities import (
    EvaluationSample,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _sample(
    *,
    sample_id: str,
    category: str,
    level: Level,
) -> EvaluationSample:
    return EvaluationSample(
        sample_id=sample_id,
        question_id=f"question-{sample_id}",
        question="What is RAG?",
        candidate_answer="Answer",
        expected_answer="Expected",
        category=category,
        level=level,
    )


def _dataset() -> EvaluationDataset:
    return EvaluationDataset(
        dataset_id="dataset-1",
        dataset_name="Benchmark Dataset",
        dataset_version=DatasetVersion(
            version="1.0.0",
            stage=DatasetStage.DEVELOPMENT,
            created_by="system",
            description="Initial dataset.",
        ),
        description="Dataset description.",
        metadata=DatasetMetadata(
            created_at=datetime.utcnow(),
            rubric_version="1.0.0",
            evaluator_version="1.0.0",
            source="unit-test",
        ),
        samples=(
            _sample(
                sample_id="sample-1",
                category="RAG",
                level=Level.JR,
            ),
            _sample(
                sample_id="sample-2",
                category="RAG",
                level=Level.MID,
            ),
            _sample(
                sample_id="sample-3",
                category="Agents",
                level=Level.MID,
            ),
        ),
    )


def test_dataset_distribution_analyzer_should_build_snapshot_without_splits() -> None:
    snapshot = DatasetDistributionAnalyzer.analyze(
        dataset=_dataset(),
    )

    assert isinstance(
        snapshot,
        DatasetDistributionSnapshot,
    )

    assert snapshot.dataset_id == "dataset-1"

    assert snapshot.sample_count == 3

    assert snapshot.category_distribution == {
        "RAG": 2,
        "Agents": 1,
    }

    assert snapshot.level_distribution == {
        "JR": 1,
        "MID": 2,
    }

    assert snapshot.split_distribution == {
        "UNSPLIT": 3,
    }


def test_dataset_distribution_analyzer_should_build_snapshot_with_splits() -> None:
    dataset = _dataset()

    splits = (
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(
                "sample-1",
                "sample-2",
            ),
        ),
        DatasetSplit(
            split_type=DatasetSplitType.TEST,
            sample_ids=(
                "sample-3",
            ),
        ),
    )

    snapshot = DatasetDistributionAnalyzer.analyze(
        dataset=dataset,
        splits=splits,
    )

    assert snapshot.split_distribution == {
        "TRAIN": 2,
        "TEST": 1,
    }


def test_dataset_distribution_analyzer_should_raise_for_duplicate_split_samples() -> None:
    dataset = _dataset()

    splits = (
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(
                "sample-1",
                "sample-2",
            ),
        ),
        DatasetSplit(
            split_type=DatasetSplitType.TEST,
            sample_ids=(
                "sample-2",
                "sample-3",
            ),
        ),
    )

    with pytest.raises(
        EvaluationValidationError,
        match="split sample_ids must be unique",
    ):
        DatasetDistributionAnalyzer.analyze(
            dataset=dataset,
            splits=splits,
        )


def test_dataset_distribution_analyzer_should_raise_for_unknown_sample_ids() -> None:
    dataset = _dataset()

    splits = (
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(
                "sample-1",
                "sample-2",
            ),
        ),
        DatasetSplit(
            split_type=DatasetSplitType.TEST,
            sample_ids=(
                "unknown-sample",
            ),
        ),
    )

    with pytest.raises(
        EvaluationValidationError,
        match="unknown dataset samples",
    ):
        DatasetDistributionAnalyzer.analyze(
            dataset=dataset,
            splits=splits,
        )


def test_dataset_distribution_analyzer_should_raise_for_missing_split_coverage() -> None:
    dataset = _dataset()

    splits = (
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(
                "sample-1",
            ),
        ),
        DatasetSplit(
            split_type=DatasetSplitType.TEST,
            sample_ids=(
                "sample-2",
            ),
        ),
    )

    with pytest.raises(
        EvaluationValidationError,
        match="do not cover all dataset samples",
    ):
        DatasetDistributionAnalyzer.analyze(
            dataset=dataset,
            splits=splits,
        )