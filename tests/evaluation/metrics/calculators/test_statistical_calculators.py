from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.cohens_dz_calculator import (
    CohensDzCalculator,
)
from src.evaluation.metrics.calculators.confidence_interval_calculator import (
    ConfidenceIntervalCalculator,
)
from src.evaluation.metrics.calculators.paired_difference_calculator import (
    PairedDifferenceCalculator,
)
from src.evaluation.metrics.calculators.paired_t_statistic_calculator import (
    PairedTStatisticCalculator,
)
from src.evaluation.metrics.calculators.paired_t_test_calculator import (
    PairedTTestCalculator,
)
from src.evaluation.metrics.calculators.pearson_coefficient_calculator import (
    PearsonCoefficientCalculator,
)
from src.evaluation.metrics.calculators.sample_standard_deviation_calculator import (
    SampleStandardDeviationCalculator,
)


def test_paired_difference_calculator_should_return_after_minus_before() -> None:
    differences = PairedDifferenceCalculator.calculate(
        before_values=(1.0, 2.0, 4.0),
        after_values=(2.0, 5.0, 7.0),
    )

    assert differences == (1.0, 3.0, 3.0)


def test_sample_standard_deviation_calculator_should_calculate_sample_stdev() -> None:
    result = SampleStandardDeviationCalculator.calculate(
        values=(2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0),
    )

    assert result == pytest.approx(2.138089935)


def test_pearson_coefficient_calculator_should_calculate_perfect_negative_correlation() -> None:
    result = PearsonCoefficientCalculator.calculate(
        x_values=(1.0, 2.0, 3.0),
        y_values=(3.0, 2.0, 1.0),
    )

    assert result == pytest.approx(-1.0)


def test_pearson_coefficient_calculator_should_raise_for_constant_values() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="Pearson correlation is undefined for constant values",
    ):
        PearsonCoefficientCalculator.calculate(
            x_values=(1.0, 1.0, 1.0),
            y_values=(2.0, 3.0, 4.0),
        )


def test_paired_t_statistic_calculator_should_calculate_statistic() -> None:
    result = PairedTStatisticCalculator.calculate(
        differences=(1.0, 2.0, 3.0),
    )

    assert result == pytest.approx(3.464101615)


def test_cohens_dz_calculator_should_calculate_effect_size() -> None:
    result = CohensDzCalculator.calculate(
        differences=(1.0, 2.0, 3.0),
    )

    assert result == pytest.approx(2.0)


def test_paired_t_test_calculator_should_return_significance_result() -> None:
    result = PairedTTestCalculator.calculate(
        before_values=(1.0, 2.0, 3.0),
        after_values=(2.0, 4.0, 6.0),
        p_value=0.01,
        notes="paired smoke test",
    )

    assert result.test_name == "paired_t_test"
    assert result.statistic == pytest.approx(3.464101615)
    assert result.effect_size == pytest.approx(2.0)
    assert result.is_significant is True
    assert result.rejects_null_hypothesis is True
    assert result.retains_null_hypothesis is False
    assert result.sample_count == 3
    assert result.notes == "paired smoke test"


def test_paired_t_test_calculator_should_raise_for_mismatched_lengths() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="before_values and after_values must have the same length",
    ):
        PairedTTestCalculator.calculate(
            before_values=(1.0, 2.0),
            after_values=(2.0,),
            p_value=0.01,
        )


def test_confidence_interval_calculator_should_calculate_interval() -> None:
    interval = ConfidenceIntervalCalculator().calculate(
        values=(10.0, 12.0, 14.0),
        confidence_level=0.95,
        z_score=1.96,
    )

    assert interval.lower_bound == pytest.approx(9.736786)
    assert interval.upper_bound == pytest.approx(14.263214)
    assert interval.midpoint == pytest.approx(12.0)
    assert interval.margin_of_error == pytest.approx(2.263214)
    assert interval.contains(12.0) is True
