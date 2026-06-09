from __future__ import annotations

from statistics import mean

from src.evaluation.metrics.calculators.bootstrap_standard_deviation_calculator import (
    BootstrapStandardDeviationCalculator,
)
from src.evaluation.metrics.calculators.confidence_interval_calculator import (
    ConfidenceIntervalCalculator,
)
from src.evaluation.metrics.value_objects.bootstrap_distribution_summary import (
    BootstrapDistributionSummary,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)


class BootstrapDistributionSummaryBuilder:
    """
    Builds bootstrap distribution summaries.
    """

    def __init__(
        self,
        *,
        confidence_interval_calculator: (
            ConfidenceIntervalCalculator | None
        ) = None,
    ) -> None:
        self._confidence_interval_calculator = (
            confidence_interval_calculator
            or ConfidenceIntervalCalculator()
        )

    def build(
        self,
        *,
        metric_name: str,
        bootstrap_samples: tuple[BootstrapSampleResult, ...],
        notes: str | None = None,
    ) -> BootstrapDistributionSummary:
        statistic_values = tuple(
            sample.statistic_value
            for sample in bootstrap_samples
        )

        return BootstrapDistributionSummary(
            metric_name=metric_name,
            bootstrap_iterations=len(bootstrap_samples),
            mean_score=mean(statistic_values),
            std_deviation=(
                BootstrapStandardDeviationCalculator.calculate(
                    statistic_values=statistic_values,
                )
            ),
            min_score=min(statistic_values),
            max_score=max(statistic_values),
            confidence_interval=(
                self._confidence_interval_calculator.calculate(
                    values=statistic_values,
                )
            ),
            bootstrap_samples=bootstrap_samples,
            notes=notes,
        )