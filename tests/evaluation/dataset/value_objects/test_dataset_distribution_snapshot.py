from __future__ import annotations

import pytest

from src.evaluation.dataset.entities.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _valid_snapshot_kwargs() -> dict:
    return {
        "dataset_id": "dataset-1",
        "sample_count": 10,
        "category_distribution": {
            "RAG": 6,
            "Agents": 4,
        },
        "level_distribution": {
            "JR": 3,
            "MID": 4,
            "SENIOR": 3,
        },
        "split_distribution": {
            "TRAIN": 7,
            "VALIDATION": 2,
            "TEST": 1,
        },
    }


def test_dataset_distribution_snapshot_should_create_successfully() -> None:
    snapshot = DatasetDistributionSnapshot(
        **_valid_snapshot_kwargs(),
    )

    assert snapshot.dataset_id == "dataset-1"
    assert snapshot.sample_count == 10
    assert snapshot.category_count == 2
    assert snapshot.level_count == 3
    assert snapshot.split_count == 3


def test_dataset_distribution_snapshot_should_raise_for_empty_dataset_id() -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs["dataset_id"] = ""

    with pytest.raises(
        EvaluationValidationError,
        match="dataset_id cannot be empty",
    ):
        DatasetDistributionSnapshot(**kwargs)


def test_dataset_distribution_snapshot_should_raise_for_negative_sample_count() -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs["sample_count"] = -1

    with pytest.raises(
        EvaluationValidationError,
        match="sample_count must be greater than or equal to 0",
    ):
        DatasetDistributionSnapshot(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "category_distribution",
        "level_distribution",
        "split_distribution",
    ],
)
def test_dataset_distribution_snapshot_should_raise_for_empty_distribution(
    field_name: str,
) -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs[field_name] = {}

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be empty",
    ):
        DatasetDistributionSnapshot(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "category_distribution",
        "level_distribution",
        "split_distribution",
    ],
)
def test_dataset_distribution_snapshot_should_raise_for_invalid_distribution_type(
    field_name: str,
) -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs[field_name] = []

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} must be dict",
    ):
        DatasetDistributionSnapshot(**kwargs)


def test_dataset_distribution_snapshot_should_be_immutable() -> None:
    snapshot = DatasetDistributionSnapshot(
        **_valid_snapshot_kwargs(),
    )

    with pytest.raises(
        AttributeError,
    ):
        snapshot.dataset_id = "changed"  # type: ignore[misc]