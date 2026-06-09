from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.cohens_dz_calculator import (
    CohensDzCalculator,
)
from src.evaluation.metrics.calculators.paired_difference_calculator import (
    PairedDifferenceCalculator,
)
from src.evaluation.metrics.calculators.paired_t_statistic_calculator import (
    PairedTStatisticCalculator,
)
from src.evaluation.metrics.constants.statistical_tests import (
    DEFAULT_ALPHA,
    PAIRED_T_TEST_NAME,
)
from src.evaluation.metrics.validators.paired_t_test_input_validator import (
    PairedTTestInputValidator,
)
from src.evaluation.metrics.value_objects.significance_test_result import (
    SignificanceTestResult,
)


class PairedTTestCalculator:
    """
    Paired t-test orchestration calculator.
    """

    @staticmethod
    def calculate(
        *,
        before_values: Sequence[float],
        after_values: Sequence[float],
        p_value: float,
        alpha: float = DEFAULT_ALPHA,
        interpretation: str | None = None,
        notes: str | None = None,
    ) -> SignificanceTestResult:
        PairedTTestInputValidator.validate(
            before_values=before_values,
            after_values=after_values,
            p_value=p_value,
            alpha=alpha,
        )

        differences = PairedDifferenceCalculator.calculate(
            before_values=before_values,
            after_values=after_values,
        )

        statistic = PairedTStatisticCalculator.calculate(
            differences=differences,
        )

        effect_size = CohensDzCalculator.calculate(
            differences=differences,
        )

        return SignificanceTestResult(
            test_name=PAIRED_T_TEST_NAME,
            statistic=statistic,
            p_value=p_value,
            alpha=alpha,
            is_significant=(
                p_value
                < alpha
            ),
            sample_count=len(differences),
            effect_size=effect_size,
            interpretation=interpretation,
            notes=notes,
        )