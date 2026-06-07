from __future__ import annotations

import pytest

from src.evaluation.dataset.value_objects.dataset_drift_snapshot import (
    DatasetDriftSnapshot,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _valid_snapshot_kwargs() -> dict:
    return {
        "baseline_dataset_id": "dataset-v1",
        "comparison_dataset_id": "dataset-v2",
        "sample_count_delta": 5,
        "category_drift": {
            "RAG": 0.12,
            "Agents": 0.05,
        },
        "level_drift": {
            "JR": 0.10,
            "MID": 0.04,
        },
        "split_drift": {
            "TRAIN": 0.03,
            "TEST": 0.08,
        },
        "overall_drift_score": 0.12,
        "drift_detected": True,
        "notes": "Moderate dataset drift detected.",
    }


def test_dataset_drift_snapshot_should_create_successfully() -> None:
    snapshot = DatasetDriftSnapshot(
        **_valid_snapshot_kwargs(),
    )

    assert snapshot.baseline_dataset_id == "dataset-v1"
    assert snapshot.comparison_dataset_id == "dataset-v2"
    assert snapshot.sample_count_delta == 5
    assert snapshot.category_count == 2
    assert snapshot.level_count == 2
    assert snapshot.split_count == 2
    assert snapshot.overall_drift_score == 0.12
    assert snapshot.drift_detected is True
    assert snapshot.notes == "Moderate dataset drift detected."


@pytest.mark.parametrize(
    "field_name",
    [
        "baseline_dataset_id",
        "comparison_dataset_id",
    ],
)
def test_dataset_drift_snapshot_should_raise_for_empty_dataset_ids(
    field_name: str,
) -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be empty",
    ):
        DatasetDriftSnapshot(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "category_drift",
        "level_drift",
        "split_drift",
    ],
)
def test_dataset_drift_snapshot_should_raise_for_invalid_drift_type(
    field_name: str,
) -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs[field_name] = []

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} must be dict",
    ):
        DatasetDriftSnapshot(**kwargs)


@pytest.mark.parametrize(
    "field_name",
    [
        "category_drift",
        "level_drift",
        "split_drift",
    ],
)
def test_dataset_drift_snapshot_should_raise_for_empty_drift_map(
    field_name: str,
) -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs[field_name] = {}

    with pytest.raises(
        EvaluationValidationError,
        match=f"{field_name} cannot be empty",
    ):
        DatasetDriftSnapshot(**kwargs)


def test_dataset_drift_snapshot_should_raise_for_invalid_overall_drift_score() -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs["overall_drift_score"] = 1.1

    with pytest.raises(
        EvaluationValidationError,
        match=(
            "overall_drift_score must be less than "
            "or equal to 1"
        ),
    ):
        DatasetDriftSnapshot(**kwargs)


def test_dataset_drift_snapshot_should_raise_for_invalid_drift_detected_type() -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs["drift_detected"] = "yes"

    with pytest.raises(
        EvaluationValidationError,
        match="drift_detected must be bool",
    ):
        DatasetDriftSnapshot(**kwargs)


def test_dataset_drift_snapshot_should_raise_for_invalid_notes_type() -> None:
    kwargs = _valid_snapshot_kwargs()
    kwargs["notes"] = 123

    with pytest.raises(
        EvaluationValidationError,
        match="notes must be str",
    ):
        DatasetDriftSnapshot(**kwargs)


def test_dataset_drift_snapshot_should_be_immutable() -> None:
    snapshot = DatasetDriftSnapshot(
        **_valid_snapshot_kwargs(),
    )

    with pytest.raises(
        AttributeError,
    ):
        snapshot.baseline_dataset_id = "changed"  # type: ignore[misc]