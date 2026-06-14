from __future__ import annotations

from src.evaluation.rag.calculators.rag_report_count_calculator import RAGReportCountCalculator
from tests.evaluation.rag.factories import rag_result


def test_rag_report_count_should_count_samples_passes_failures_and_hallucinations() -> None:
    results = (
        rag_result(result_id="r1", passed=True, hallucination_detected=False),
        rag_result(result_id="r2", passed=False, hallucination_detected=True),
        rag_result(result_id="r3", passed=True, hallucination_detected=True),
    )

    assert RAGReportCountCalculator.sample_count(results=results) == 3
    assert RAGReportCountCalculator.passed_count(results=results) == 2
    assert RAGReportCountCalculator.failed_count(results=results) == 1
    assert RAGReportCountCalculator.hallucination_count(results=results) == 2
