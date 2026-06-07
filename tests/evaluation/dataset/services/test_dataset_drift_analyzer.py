from __future__ import annotations

import pytest

from src.evaluation.dataset.entities.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.dataset.services.dataset_drift_analyzer import (
    DatasetDriftAnalyzer,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


def _snapshot(
    *,
    dataset_id: str,
    sample_count: int = 10,
    category_distribution: dict[str, int] | None = None,
    level_distribution: dict[str, int] | None = None,
    split_distribution: dict[str, int] | None = None,
) -> DatasetDistributionSnapshot:
    return DatasetDistributionSnapshot(
        dataset_id=dataset_id,
        sample_count=sample_count,
        category_distribution=category_distribution
        or {
            "RAG": 5,
            "Agents": 5,
        },
        level_distribution=level_distribution
        or {
            "JR": 5,
            "MID": 5,
        },
        split_distribution=split_distribution
        or {
            "TRAIN": 7,
            "VALIDATION": 2,
            "TEST": 1,
        },
    )


def test_dataset_drift_analyzer_should_create_drift_snapshot() -> None:
    baseline = _snapshot(
        dataset_id="baseline",
        category_distribution={
            "RAG": 5,
            "Agents": 5,
        },
    )

    comparison = _snapshot(
        dataset_id="comparison",
        sample_count=12,
        category_distribution={
            "RAG": 9,
            "Agents": 3,
        },
    )

    snapshot = DatasetDriftAnalyzer.analyze(
        baseline=baseline,
        comparison=comparison,
        drift_threshold=0.10,
        notes="Drift check.",
    )

    assert snapshot.baseline_dataset_id == "baseline"
    assert snapshot.comparison_dataset_id == "comparison"
    assert snapshot.sample_count_delta == 2
    assert snapshot.category_drift == {
        "Agents": 0.25,
        "RAG": 0.25,
    }
    assert snapshot.overall_drift_score == 0.25
    assert snapshot.drift_detected is True
    assert snapshot.notes == "Drift check."


def test_dataset_drift_analyzer_should_not_detect_drift_below_threshold() -> None:
    baseline = _snapshot(
        dataset_id="baseline",
    )

    comparison = _snapshot(
        dataset_id="comparison",
    )

    snapshot = DatasetDriftAnalyzer.analyze(
        baseline=baseline,
        comparison=comparison,
        drift_threshold=0.10,
    )

    assert snapshot.overall_drift_score == 0.0
    assert snapshot.drift_detected is False


def test_dataset_drift_analyzer_should_include_new_keys() -> None:
    baseline = _snapshot(
        dataset_id="baseline",
        category_distribution={
            "RAG": 10,
        },
    )

    comparison = _snapshot(
        dataset_id="comparison",
        category_distribution={
            "RAG": 5,
            "Agents": 5,
        },
    )

    snapshot = DatasetDriftAnalyzer.analyze(
        baseline=baseline,
        comparison=comparison,
    )

    assert snapshot.category_drift == {
        "Agents": 0.5,
        "RAG": 0.5,
    }


def test_dataset_drift_analyzer_should_raise_for_invalid_baseline_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="baseline must be a DatasetDistributionSnapshot",
    ):
        DatasetDriftAnalyzer.analyze(
            baseline="invalid",  # type: ignore[arg-type]
            comparison=_snapshot(
                dataset_id="comparison",
            ),
        )


def test_dataset_drift_analyzer_should_raise_for_invalid_comparison_type() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="comparison must be a DatasetDistributionSnapshot",
    ):
        DatasetDriftAnalyzer.analyze(
            baseline=_snapshot(
                dataset_id="baseline",
            ),
            comparison="invalid",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "threshold",
    [
        -0.1,
        1.1,
    ],
)
def test_dataset_drift_analyzer_should_raise_for_invalid_threshold_range(
    threshold: float,
) -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="drift_threshold must be between 0 and 1",
    ):
        DatasetDriftAnalyzer.analyze(
            baseline=_snapshot(
                dataset_id="baseline",
            ),
            comparison=_snapshot(
                dataset_id="comparison",
            ),
            drift_threshold=threshold,
        )


def test_dataset_drift_analyzer_should_raise_for_non_numeric_threshold() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="drift_threshold must be numeric",
    ):
        DatasetDriftAnalyzer.analyze(
            baseline=_snapshot(
                dataset_id="baseline",
            ),
            comparison=_snapshot(
                dataset_id="comparison",
            ),
            drift_threshold="0.1",  # type: ignore[arg-type]
        )