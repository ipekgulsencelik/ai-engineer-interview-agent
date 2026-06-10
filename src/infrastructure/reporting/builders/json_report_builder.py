from __future__ import annotations

import json

from src.domain.results.interview_report_result import (
    InterviewReportResult,
)


class JsonReportBuilder:
    """
    JSON report serialization builder.
    """

    @staticmethod
    def build(
        *,
        report: InterviewReportResult,
    ) -> str:
        payload = {
            "candidate_level": (
                report.candidate_level
            ),
            "overall_score": (
                report.overall_score
            ),
            "market_alignment_score": (
                report.market_alignment_score
            ),
            "evaluated_questions": (
                report.evaluated_questions
            ),
            "strengths": list(
                report.strengths,
            ),
            "weaknesses": list(
                report.weaknesses,
            ),
            "recommendations": list(
                report.recommendations,
            ),
            "category_scores": {
                category: score
                for category, score in (
                    report.category_scores
                )
            },
        }

        return json.dumps(
            payload,
            indent=2,
        )