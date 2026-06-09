from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.cohens_kappa_calculator import (
    CohensKappaCalculator,
)
from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.calculators.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)
from src.evaluation.metrics.services.category_metrics_analyzer import (
    CategoryMetricsAnalyzer,
)


def _analyzer() -> CategoryMetricsAnalyzer:
    return CategoryMetricsAnalyzer(
        pearson_calculator=PearsonCorrelationCalculator(),
        agreement_calculator=CohensKappaCalculator(),
        regression_calculator=RegressionMetricsCalculator(),
    )


def test_category_metrics_analyzer_should_return_snapshot_per_category() -> None:
    snapshots = _analyzer().analyze(
        human_scores=(1.0, 2.0, 3.0, 4.0),
        llm_scores=(1.1, 2.1, 2.9, 4.1),
        human_labels=("low", "medium", "medium", "high"),
        llm_labels=("low", "medium", "medium", "high"),
        categories=(" RAG ", "RAG", "MLOps", "MLOps"),
        notes="category analysis",
    )

    assert tuple(snapshot.category for snapshot in snapshots) == (
        "RAG",
        "MLOps",
    )
    assert snapshots[0].sample_count == 2
    assert snapshots[0].average_human_score == pytest.approx(1.5)
    assert snapshots[0].average_llm_score == pytest.approx(1.6)
    assert snapshots[0].notes == "category analysis"
    assert snapshots[1].sample_count == 2
    assert snapshots[1].average_human_score == pytest.approx(3.5)


def test_category_metrics_analyzer_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="llm_scores and categories must have the same length",
    ):
        _analyzer().analyze(
            human_scores=(1.0, 2.0),
            llm_scores=(1.0,),
            human_labels=("low", "high"),
            llm_labels=("low", "high"),
            categories=("RAG", "RAG"),
        )
