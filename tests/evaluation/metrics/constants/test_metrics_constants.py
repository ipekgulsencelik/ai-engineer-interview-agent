from __future__ import annotations

from src.evaluation.metrics.constants import agreements, alignment, alignment_thresholds
from src.evaluation.metrics.constants import benchmark, benchmark_trends, bootstrap
from src.evaluation.metrics.constants import category_metrics, confidence_intervals
from src.evaluation.metrics.constants import correlations, regression_metrics
from src.evaluation.metrics.constants import statistical_tests, statistical_thresholds


def test_alignment_threshold_compatibility_module_should_match_alignment_constants() -> (
    None
):
    assert (
        alignment_thresholds.STRONG_ALIGNMENT_THRESHOLD
        == alignment.STRONG_ALIGNMENT_THRESHOLD
    )
    assert (
        alignment_thresholds.MODERATE_ALIGNMENT_THRESHOLD
        == alignment.MODERATE_ALIGNMENT_THRESHOLD
    )
    assert alignment_thresholds.MIN_ALIGNMENT_SCORE == alignment.MIN_ALIGNMENT_SCORE
    assert alignment_thresholds.MAX_ALIGNMENT_SCORE == alignment.MAX_ALIGNMENT_SCORE


def test_metrics_threshold_constants_should_be_ordered_consistently() -> None:
    assert alignment.MAX_ALIGNMENT_SCORE > alignment.STRONG_ALIGNMENT_THRESHOLD
    assert alignment.STRONG_ALIGNMENT_THRESHOLD > alignment.MODERATE_ALIGNMENT_THRESHOLD
    assert alignment.MODERATE_ALIGNMENT_THRESHOLD > alignment.MIN_ALIGNMENT_SCORE
    assert benchmark.STRONG_BENCHMARK_THRESHOLD > benchmark.MODERATE_BENCHMARK_THRESHOLD
    assert (
        correlations.VERY_STRONG_CORRELATION_THRESHOLD
        > correlations.STRONG_CORRELATION_THRESHOLD
    )
    assert (
        correlations.STRONG_CORRELATION_THRESHOLD
        > correlations.MODERATE_CORRELATION_THRESHOLD
    )
    assert (
        correlations.MODERATE_CORRELATION_THRESHOLD
        > correlations.WEAK_CORRELATION_THRESHOLD
    )
    assert (
        regression_metrics.EXCELLENT_R2_THRESHOLD > regression_metrics.GOOD_R2_THRESHOLD
    )
    assert (
        regression_metrics.GOOD_R2_THRESHOLD > regression_metrics.MODERATE_R2_THRESHOLD
    )


def test_metrics_bound_constants_should_define_valid_ranges() -> None:
    assert agreements.AGREEMENT_MIN_RATIO == 0.0
    assert agreements.AGREEMENT_MAX_RATIO == 1.0
    assert correlations.CORRELATION_MIN_VALUE == -1.0
    assert correlations.CORRELATION_MAX_VALUE == 1.0
    assert confidence_intervals.MIN_CONFIDENCE_LEVEL == 0.0
    assert confidence_intervals.MAX_CONFIDENCE_LEVEL == 1.0
    assert statistical_tests.MIN_P_VALUE == 0.0
    assert statistical_tests.MAX_P_VALUE == 1.0
    assert statistical_thresholds.MIN_SCORE == 0.0
    assert statistical_thresholds.MAX_SCORE == 1.0


def test_operational_constants_should_match_expected_defaults() -> None:
    assert bootstrap.DEFAULT_BOOTSTRAP_ITERATIONS == 1000
    assert bootstrap.DEFAULT_BOOTSTRAP_SEED == 42
    assert bootstrap.MIN_BOOTSTRAP_ITERATIONS == 1
    assert category_metrics.NEUTRAL_SCORE_DELTA == 0.0
    assert statistical_tests.PAIRED_T_TEST_NAME == "paired_t_test"
    assert benchmark_trends.VALID_TREND_DIRECTIONS == frozenset(
        {"improving", "stable", "degrading"}
    )
