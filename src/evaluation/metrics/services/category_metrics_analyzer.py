from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.builders.category_metric_snapshot_builder import (
    CategoryMetricSnapshotBuilder,
)
from src.evaluation.metrics.calculators.cohen_kappa_calculator import (
    CohenKappaCalculator,
)
from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.calculators.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)
from src.evaluation.metrics.constants.alignment import (
    HUMAN_LLM_AGREEMENT_METRIC_NAME,
    HUMAN_LLM_REGRESSION_METRIC_NAME,
    HUMAN_SCORE_METRIC_NAME,
    LLM_SCORE_METRIC_NAME,
)
from src.evaluation.metrics.groupers.category_index_grouper import (
    CategoryIndexGrouper,
)
from src.evaluation.metrics.validators.category_metrics_input_validator import (
    CategoryMetricsInputValidator,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


class CategoryMetricsAnalyzer:
    """
    Category-level metrics analyzer.

    Orchestrates category grouping, metric calculation,
    and snapshot construction.
    """

    def __init__(
        self,
        *,
        pearson_calculator: PearsonCorrelationCalculator,
        agreement_calculator: CohenKappaCalculator,
        regression_calculator: RegressionMetricsCalculator,
    ) -> None:
        self._pearson_calculator = pearson_calculator
        self._agreement_calculator = agreement_calculator
        self._regression_calculator = regression_calculator

    def analyze(
        self,
        *,
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
        categories: Sequence[str],
        notes: str | None = None,
    ) -> tuple[CategoryMetricSnapshot, ...]:
        CategoryMetricsInputValidator.validate(
            human_scores=human_scores,
            llm_scores=llm_scores,
            human_labels=human_labels,
            llm_labels=llm_labels,
            categories=categories,
        )

        grouped_indices = CategoryIndexGrouper.group(
            categories=categories,
        )

        snapshots: list[CategoryMetricSnapshot] = []

        for category, indices in grouped_indices.items():
            snapshot = self._analyze_category(
                category=category,
                indices=indices,
                human_scores=human_scores,
                llm_scores=llm_scores,
                human_labels=human_labels,
                llm_labels=llm_labels,
                notes=notes,
            )

            snapshots.append(snapshot)

        return tuple(snapshots)

    def _analyze_category(
        self,
        *,
        category: str,
        indices: tuple[int, ...],
        human_scores: Sequence[float],
        llm_scores: Sequence[float],
        human_labels: Sequence[str],
        llm_labels: Sequence[str],
        notes: str | None,
    ) -> CategoryMetricSnapshot:
        category_human_scores = tuple(
            human_scores[index]
            for index in indices
        )

        category_llm_scores = tuple(
            llm_scores[index]
            for index in indices
        )

        category_human_labels = tuple(
            human_labels[index]
            for index in indices
        )

        category_llm_labels = tuple(
            llm_labels[index]
            for index in indices
        )

        correlation_result = self._pearson_calculator.calculate(
            metric_x=HUMAN_SCORE_METRIC_NAME,
            metric_y=LLM_SCORE_METRIC_NAME,
            x_values=category_human_scores,
            y_values=category_llm_scores,
        )

        agreement_result = self._agreement_calculator.calculate(
            metric_name=HUMAN_LLM_AGREEMENT_METRIC_NAME,
            evaluator_a_labels=category_human_labels,
            evaluator_b_labels=category_llm_labels,
        )

        regression_result = self._regression_calculator.calculate(
            metric_name=HUMAN_LLM_REGRESSION_METRIC_NAME,
            actual_values=category_human_scores,
            predicted_values=category_llm_scores,
        )

        return CategoryMetricSnapshotBuilder.build(
            category=category,
            human_scores=category_human_scores,
            llm_scores=category_llm_scores,
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
            notes=notes,
        )