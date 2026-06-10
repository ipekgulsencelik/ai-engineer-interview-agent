from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.benchmark_evaluation_report_builder import (
    BenchmarkEvaluationReportBuilder,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)


def test_benchmark_evaluation_report_builder_should_build_report() -> None:
    report = BenchmarkEvaluationReportBuilder.build(
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
