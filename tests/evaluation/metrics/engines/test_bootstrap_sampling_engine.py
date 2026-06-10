from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.engines.bootstrap_sampling_engine import (
    BootstrapSamplingEngine,
)
from src.evaluation.metrics.value_objects.bootstrap_distribution_summary import (
    BootstrapDistributionSummary,
)


def test_bootstrap_sampling_engine_should_generate_reproducible_summary() -> None:
    summary = BootstrapSamplingEngine().run(
        metric_name="mean_score",
        values=(10.0, 20.0, 30.0),
        bootstrap_iterations=5,
        seed=7,
        notes="bootstrap test",
    )

    assert isinstance(summary, BootstrapDistributionSummary)
    assert summary.metric_name == "mean_score"
    assert summary.bootstrap_iterations == 5
    assert tuple(sample.statistic_value for sample in summary.bootstrap_samples) == pytest.approx(
        (
            16.666666667,
            16.666666667,
            20.0,
            23.333333333,
            10.0,
        )
    )
    assert summary.mean_score == pytest.approx(17.333333333)
    assert summary.notes == "bootstrap test"


def test_bootstrap_sampling_engine_should_raise_for_empty_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="values cannot be empty",
    ):
        BootstrapSamplingEngine().run(
            metric_name="mean_score",
            values=(),
            bootstrap_iterations=5,
        )
