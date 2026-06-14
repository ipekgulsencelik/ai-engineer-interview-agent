from __future__ import annotations

from src.evaluation.rag.interpreters.rag_report_interpreter import RAGReportInterpreter


def test_rag_report_interpreter_should_mark_report_passed_when_no_failures() -> None:
    assert RAGReportInterpreter().interpret(sample_count=2, failed_count=0) == "rag_report_passed"


def test_rag_report_interpreter_should_mark_report_failed_when_failures_exist() -> None:
    assert RAGReportInterpreter().interpret(sample_count=2, failed_count=1) == "rag_report_failed"
