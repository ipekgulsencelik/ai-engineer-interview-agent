from __future__ import annotations

from src.infrastructure.reporting.formatters.markdown_list_formatter import (
    MarkdownListFormatter,
)
from src.domain.results.interview_report_result import (
    InterviewReportResult,
)


class MarkdownReportBuilder:
    """
    Markdown interview report builder.
    """

    @staticmethod
    def build(
        *,
        report: InterviewReportResult,
    ) -> str:
        strengths = (
            MarkdownListFormatter.format(
                items=report.strengths,
            )
        )

        weaknesses = (
            MarkdownListFormatter.format(
                items=report.weaknesses,
            )
        )

        recommendations = (
            MarkdownListFormatter.format(
                items=report.recommendations,
            )
        )

        return f"""
        # AI Engineer Interview Report

        ## Summary

        - Candidate Level: {report.candidate_level}
        - Overall Score: {report.overall_score:.2f}/10
        - Market Alignment: {report.market_alignment_score:.2f}
        - Evaluated Questions: {report.evaluated_questions}

        ## Strengths

        {strengths}

        ## Weaknesses

        {weaknesses}

        ## Recommendations

        {recommendations}
        """.strip()