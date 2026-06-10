from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.bootstrap_distribution_summary_builder import (
    BootstrapDistributionSummaryBuilder,
)
from src.evaluation.metrics.value_objects.bootstrap_distribution_summary import (
    BootstrapDistributionSummary,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)


def test_bootstrap_distribution_summary_builder_should_aggregate_samples() -> None:
    summary = BootstrapDistributionSummaryBuilder().build(
        metric_name="alignment_score",
        bootstrap_samples=(
            BootstrapSampleResult(
                sample_index=0,
                sample_size=3,
                statistic_value=10.0,
                seed=42,
            ),
            BootstrapSampleResult(
                sample_index=1,
                sample_size=3,
                statistic_value=12.0,
                seed=42,
            ),
            BootstrapSampleResult(
                sample_index=2,
                sample_size=3,
                statistic_value=14.0,
                seed=42,
            ),
        ),
        notes="summary test",
    )

    assert isinstance(summary, BootstrapDistributionSummary)
    assert summary.metric_name == "alignment_score"
    assert summary.bootstrap_iterations == 3
    assert summary.mean_score == pytest.approx(12.0)
    assert summary.std_deviation == pytest.approx(2.0)
    assert summary.min_score == pytest.approx(10.0)
    assert summary.max_score == pytest.approx(14.0)
    assert summary.score_range == pytest.approx(4.0)
    assert summary.has_samples is True
    assert summary.confidence_interval.midpoint == pytest.approx(12.0)
    assert summary.notes == "summary test"
