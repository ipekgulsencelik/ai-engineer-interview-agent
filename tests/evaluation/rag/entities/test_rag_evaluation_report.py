from __future__ import annotations

from tests.evaluation.rag.factories import rag_report


def test_rag_evaluation_report_should_expose_result_and_failure_flags() -> None:
    report = rag_report()
    assert report.has_results is True
    assert report.has_failures is False
    assert report.all_passed is True
