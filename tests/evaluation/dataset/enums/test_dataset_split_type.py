from __future__ import annotations

from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)


def test_dataset_split_type_values() -> None:
    assert DatasetSplitType.values() == (
        "TRAIN",
        "VALIDATION",
        "TEST",
    )


def test_dataset_split_type_from_string() -> None:
    assert (
        DatasetSplitType.from_string(
            "train",
        )
        is DatasetSplitType.TRAIN
    )


def test_dataset_split_type_is_train() -> None:
    assert DatasetSplitType.TRAIN.is_train
    assert not DatasetSplitType.TRAIN.is_validation
    assert not DatasetSplitType.TRAIN.is_test


def test_dataset_split_type_is_validation() -> None:
    assert DatasetSplitType.VALIDATION.is_validation


def test_dataset_split_type_is_test() -> None:
    assert DatasetSplitType.TEST.is_test