from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.benchmark_evaluation_report_builder import (
    BenchmarkEvaluationReportBuilder,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)


class _FakeBenchmarkScoreCalculator:
    def calculate(
        self,
        *,
        alignment_report: EvaluatorAlignmentReport,
        category_snapshots: tuple[CategoryMetricSnapshot, ...],
    ) -> float:
        return 0.65


class _FakeBenchmarkInterpreter:
    def interpret(
        self,
        *,
        benchmark_score: float,
    ) -> str:
        return f"fake_benchmark_{benchmark_score:.2f}"


def test_benchmark_evaluation_report_builder_should_build_report() -> None:
    report = BenchmarkEvaluationReportBuilder().build(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(
                category="RAG",
                score=0.90,
            ),
            _category_snapshot(
                category="Agents",
                score=0.70,
            ),
        ),
        notes="Builder test.",
    )

    assert isinstance(report, BenchmarkEvaluationReport)
    assert report.benchmark_id == "benchmark-1"
    assert report.overall_score == pytest.approx(0.80)
    assert report.interpretation == "strong_benchmark"
    assert report.notes == "Builder test."


def test_benchmark_evaluation_report_builder_should_use_injected_dependencies() -> None:
    report = BenchmarkEvaluationReportBuilder(
        score_calculator=_FakeBenchmarkScoreCalculator(),
        benchmark_interpreter=_FakeBenchmarkInterpreter(),
    ).build(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(),
    )

    assert report.overall_score == pytest.approx(0.65)
    assert report.interpretation == "fake_benchmark_0.65"
