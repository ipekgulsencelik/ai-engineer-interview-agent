from __future__ import annotations


class RAGReportInterpreter:
    """
    Builds interpretation labels for RAG reports.
    """

    @staticmethod
    def interpret(
        *,
        sample_count: int,
        failed_count: int,
    ) -> str:
        if (
            sample_count > 0
            and failed_count == 0
        ):
            return "rag_report_passed"

        return "rag_report_failed"