from __future__ import annotations

import pytest

from src.evaluation.dataset.value_objects.dataset_split import (
    DatasetSplit,
)
from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def test_dataset_split_should_create_successfully() -> None:
    split = DatasetSplit(
        split_type=DatasetSplitType.TRAIN,
        sample_ids=(
            "sample-1",
            "sample-2",
        ),
    )

    assert split.split_type is DatasetSplitType.TRAIN
    assert split.sample_ids == (
        "sample-1",
        "sample-2",
    )
    assert split.sample_count == 2
    assert split.sample_id_set == frozenset(
        {
            "sample-1",
            "sample-2",
        }
    )


def test_dataset_split_should_return_true_when_sample_exists() -> None:
    split = DatasetSplit(
        split_type=DatasetSplitType.TEST,
        sample_ids=(
            "sample-1",
            "sample-2",
        ),
    )

    assert split.contains(
        sample_id="sample-1",
    )


def test_dataset_split_should_return_false_when_sample_does_not_exist() -> None:
    split = DatasetSplit(
        split_type=DatasetSplitType.TEST,
        sample_ids=(
            "sample-1",
            "sample-2",
        ),
    )

    assert not split.contains(
        sample_id="sample-999",
    )


def test_dataset_split_should_raise_for_invalid_split_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="split_type must be a DatasetSplitType",
    ):
        DatasetSplit(
            split_type="TRAIN",  # type: ignore[arg-type]
            sample_ids=(
                "sample-1",
            ),
        )


def test_dataset_split_should_raise_for_empty_sample_ids() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_ids cannot be empty",
    ):
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(),
        )


def test_dataset_split_should_raise_for_duplicate_sample_ids() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_ids must be unique",
    ):
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(
                "sample-1",
                "sample-1",
            ),
        )


def test_dataset_split_should_raise_for_invalid_sample_ids_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_ids must be tuple",
    ):
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=["sample-1"],  # type: ignore[arg-type]
        )


def test_dataset_split_should_raise_for_invalid_sample_id_item() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"sample_ids\[0\] must be str",
    ):
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=(123,),  # type: ignore[arg-type]
        )


def test_dataset_split_should_raise_for_empty_sample_id_item() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match=r"sample_ids\[0\] cannot be empty",
    ):
        DatasetSplit(
            split_type=DatasetSplitType.TRAIN,
            sample_ids=("   ",),
        )


def test_dataset_split_should_be_immutable() -> None:
    split = DatasetSplit(
        split_type=DatasetSplitType.TRAIN,
        sample_ids=(
            "sample-1",
        ),
    )

    with pytest.raises(
        AttributeError,
    ):
        split.sample_ids = ()  # type: ignore[misc]