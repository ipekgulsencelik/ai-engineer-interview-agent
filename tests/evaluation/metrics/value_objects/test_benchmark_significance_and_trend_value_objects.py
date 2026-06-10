from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from src.evaluation.metrics.value_objects.significance_test_result import (
    SignificanceTestResult,
)
from src.evaluation.metrics.value_objects.trend_data_point import TrendDataPoint
from src.evaluation.metrics.value_objects.trend_visualization_snapshot import (
    TrendVisualizationSnapshot,
)


def test_benchmark_aggregate_result_should_expose_derived_trend_properties() -> None:
    result = BenchmarkAggregateResult(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        experiment_count=3,
        mean_score=0.80,
        median_score=0.80,
        min_score=0.70,
        max_score=0.90,
        std_deviation=0.10,
        trend_direction="improving",
        best_experiment_id="experiment-3",
        worst_experiment_id="experiment-1",
        interpretation="strong_benchmark",
    )

    assert result.score_range == pytest.approx(0.20)
    assert result.has_variance is True
    assert result.is_improving is True
    assert result.is_stable is False
    assert result.is_degrading is False


def test_significance_test_result_should_expose_hypothesis_properties() -> None:
    result = SignificanceTestResult(
        test_name="paired_t_test",
        statistic=2.5,
        p_value=0.01,
        alpha=0.05,
        is_significant=True,
        sample_count=10,
        effect_size=0.80,
    )

    assert result.rejects_null_hypothesis is True
    assert result.retains_null_hypothesis is False


def test_trend_visualization_snapshot_should_expose_delta_properties() -> None:
    snapshot = TrendVisualizationSnapshot(
        title="Trend",
        description="Trend description",
        trend_direction="degrading",
        data_points=(
            TrendDataPoint(label="experiment-1", value=0.90),
            TrendDataPoint(label="experiment-2", value=0.70),
        ),
    )

    assert snapshot.point_count == 2
    assert snapshot.first_value == pytest.approx(0.90)
    assert snapshot.last_value == pytest.approx(0.70)
    assert snapshot.delta == pytest.approx(-0.20)
    assert snapshot.has_negative_trend is True
    assert snapshot.has_positive_trend is False
    assert snapshot.is_flat_trend is False


def test_trend_visualization_snapshot_should_raise_for_invalid_direction() -> None:
    with pytest.raises(EvaluationValidationError, match="trend_direction is invalid"):
        TrendVisualizationSnapshot(
            title="Trend",
            description="Trend description",
            trend_direction="sideways",
            data_points=(TrendDataPoint(label="experiment-1", value=0.90),),
        )
