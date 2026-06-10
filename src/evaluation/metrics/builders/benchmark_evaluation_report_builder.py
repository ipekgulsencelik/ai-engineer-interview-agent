from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.benchmark_aggregate_statistics_calculator import (
    BenchmarkAggregateStatisticsCalculator,
)
from src.evaluation.metrics.calculators.benchmark_score_calculator import (
    BenchmarkScoreCalculator,
)
from src.evaluation.metrics.detectors.benchmark_trend_detector import (
    BenchmarkTrendDetector,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.interpreters.benchmark_interpreter import (
    BenchmarkInterpreter,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.value_objects.benchmark_aggregate_result import (
    BenchmarkAggregateResult,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)


class BenchmarkAggregateResultBuilder:
    """
    BenchmarkAggregateResult construction service.

    Responsible only for assembling the aggregate result
    from already validated experiment snapshots.
    """

    def __init__(
        self,
        *,
        statistics_calculator: (
            BenchmarkAggregateStatisticsCalculator
        ),
        trend_detector: (
            BenchmarkTrendDetector
        ),
        benchmark_interpreter: (
            BenchmarkInterpreter
        ),
    ) -> None:
        self._statistics_calculator = (
            statistics_calculator
        )

        self._trend_detector = (
            trend_detector
        )

        self._benchmark_interpreter = (
            benchmark_interpreter
        )

    def build(
        self,
        *,
        benchmark_id: str,
        benchmark_version: str,
        snapshots: Sequence[
            ExperimentResultSnapshot
        ],
        notes: str | None = None,
    ) -> BenchmarkAggregateResult:
        scores = (
            self._statistics_calculator.calculate_scores(
                snapshots=snapshots,
            )
        )

        mean_score = (
            self._statistics_calculator.calculate_mean(
                scores=scores,
            )
        )

        best_snapshot = (
            self._statistics_calculator.find_best_snapshot(
                snapshots=snapshots,
            )
        )

        worst_snapshot = (
            self._statistics_calculator.find_worst_snapshot(
                snapshots=snapshots,
            )
        )

        return BenchmarkAggregateResult(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            experiment_count=len(
                snapshots,
            ),
            mean_score=mean_score,
            median_score=(
                self._statistics_calculator.calculate_median(
                    scores=scores,
                )
            ),
            min_score=(
                self._statistics_calculator.calculate_min(
                    scores=scores,
                )
            ),
            max_score=(
                self._statistics_calculator.calculate_max(
                    scores=scores,
                )
            ),
            std_deviation=(
                self._statistics_calculator.calculate_standard_deviation(
                    scores=scores,
                )
            ),
            trend_direction=(
                self._trend_detector.detect(
                    scores=scores,
                )
            ),
            best_experiment_id=(
                best_snapshot.experiment_id
            ),
            worst_experiment_id=(
                worst_snapshot.experiment_id
            ),
            interpretation=(
                self._benchmark_interpreter.interpret(
                    benchmark_score=mean_score,
                )
            ),
            notes=notes,
        )


class BenchmarkEvaluationReportBuilder:
    """
    Builds benchmark-level evaluation reports.
    """

    @staticmethod
    def build(
        *,
        benchmark_id: str,
        benchmark_name: str,
        dataset_id: str,
        dataset_version: str,
        model_name: str,
        evaluator_id: str,
        alignment_report: EvaluatorAlignmentReport,
        category_snapshots: tuple[CategoryMetricSnapshot, ...],
        notes: str | None = None,
    ) -> BenchmarkEvaluationReport:
        overall_score = BenchmarkScoreCalculator.calculate(
            alignment_report=alignment_report,
            category_snapshots=category_snapshots,
        )

        return BenchmarkEvaluationReport(
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            model_name=model_name,
            evaluator_id=evaluator_id,
            alignment_report=alignment_report,
            category_snapshots=category_snapshots,
            overall_score=overall_score,
            interpretation=BenchmarkInterpreter.interpret(
                benchmark_score=overall_score,
            ),
            notes=notes,
        )
