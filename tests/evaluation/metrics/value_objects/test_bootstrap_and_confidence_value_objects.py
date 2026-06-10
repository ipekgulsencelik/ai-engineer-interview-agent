from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)
from src.evaluation.metrics.value_objects.confidence_interval import (
    ConfidenceInterval,
)
from src.evaluation.metrics.value_objects.significance_test_result import (
    SignificanceTestResult,
)


def test_confidence_interval_should_expose_derived_properties() -> None:
    interval = ConfidenceInterval(
        lower_bound=10.0,
        upper_bound=14.0,
        confidence_level=0.95,
    )

    assert interval.width == pytest.approx(4.0)
    assert interval.midpoint == pytest.approx(12.0)
    assert interval.margin_of_error == pytest.approx(2.0)
    assert interval.contains(11.0) is True
    assert interval.contains(15.0) is False


def test_confidence_interval_should_raise_when_bounds_are_reversed() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="upper_bound must be greater than or equal to lower_bound",
    ):
        ConfidenceInterval(
            lower_bound=14.0,
            upper_bound=10.0,
            confidence_level=0.95,
        )


def test_bootstrap_sample_result_should_validate_sample_index() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="sample_index must be greater than or equal to 0",
    ):
        BootstrapSampleResult(
            sample_index=-1,
            sample_size=3,
            statistic_value=0.8,
            seed=42,
        )


def test_significance_test_result_should_expose_null_hypothesis_flags() -> None:
    result = SignificanceTestResult(
        test_name="paired_t_test",
        statistic=2.5,
        p_value=0.01,
        alpha=0.05,
        is_significant=True,
        sample_count=3,
        effect_size=0.9,
    )

    assert result.rejects_null_hypothesis is True
    assert result.retains_null_hypothesis is False
