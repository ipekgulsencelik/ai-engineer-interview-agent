from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.rag.builders.rag_evaluation_report_builder import RAGEvaluationReportBuilder
from tests.evaluation.rag.factories import rag_result


def test_rag_evaluation_report_builder_should_aggregate_counts_rates_and_metric_averages() -> None:
    report = RAGEvaluationReportBuilder().build(
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_name="Benchmark",
        benchmark_version="1.0.0",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="evaluator-a",
        results=(
            rag_result(result_id="r1", passed=True, hallucination_detected=False, overall_score=1.0),
            rag_result(result_id="r2", passed=False, hallucination_detected=True, overall_score=0.5),
        ),
        generated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )

    assert report.sample_count == 2
    assert report.passed_count == 1
    assert report.failed_count == 1
    assert report.hallucination_count == 1
    assert report.pass_rate == 0.5
    assert report.hallucination_rate == 0.5
    assert report.average_overall_score == 0.75
