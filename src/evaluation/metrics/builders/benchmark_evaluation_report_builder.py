from __future__ import annotations

from src.evaluation.metrics.calculators.benchmark_score_calculator import (
    BenchmarkScoreCalculator,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.interpreters.benchmark_interpreter import (
    BenchmarkInterpreter,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
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