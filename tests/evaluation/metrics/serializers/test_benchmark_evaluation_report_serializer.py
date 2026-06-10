from __future__ import annotations

import pytest

from src.evaluation.metrics.serializers.benchmark_evaluation_report_serializer import (
    BenchmarkEvaluationReportSerializer,
)
from tests.evaluation.metrics.entities.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)


def test_benchmark_evaluation_report_serializer_should_serialize_report_summary() -> (
    None
):
    report = BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(category="RAG", score=0.90),
            _category_snapshot(category="Agents", score=0.70),
        ),
        overall_score=0.80,
        interpretation="strong_benchmark",
        notes="report notes",
    )

    payload = BenchmarkEvaluationReportSerializer.serialize(report=report)

    assert payload == {
        "benchmark_id": "benchmark-1",
        "benchmark_name": "AI Engineer Benchmark",
        "dataset_id": "dataset-1",
        "dataset_version": "1.0.0",
        "model_name": "gpt-5",
        "evaluator_id": "evaluator-1",
        "overall_score": 0.80,
        "interpretation": "strong_benchmark",
        "category_count": 2,
        "sample_count": 8,
        "strongest_category": "RAG",
        "weakest_category": "Agents",
        "average_category_score": pytest.approx(0.80),
        "notes": "report notes",
    }
    assert "benchmark_version" not in payload


def test_benchmark_evaluation_report_serializer_should_handle_empty_categories() -> (
    None
):
    report = BenchmarkEvaluationReport(
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        model_name="gpt-5",
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(),
        overall_score=0.75,
        interpretation="moderate_benchmark",
    )

    payload = BenchmarkEvaluationReportSerializer.serialize(report=report)

    assert payload["category_count"] == 0
    assert payload["sample_count"] == 0
    assert payload["strongest_category"] is None
    assert payload["weakest_category"] is None
    assert payload["average_category_score"] == pytest.approx(0.0)
