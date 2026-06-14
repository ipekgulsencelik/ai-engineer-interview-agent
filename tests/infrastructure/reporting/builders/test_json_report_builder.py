from __future__ import annotations

import json

from src.domain.results.interview_report_result import InterviewReportResult
from src.infrastructure.reporting.builders.json_report_builder import JsonReportBuilder


def _report() -> InterviewReportResult:
    return InterviewReportResult(
        candidate_level="Senior",
        overall_score=8.25,
        market_alignment_score=0.91,
        evaluated_questions=6,
        strengths=("Python", "System design"),
        weaknesses=("Kubernetes depth",),
        recommendations=("Practice distributed tracing",),
        category_scores=(("backend", 8.0), ("ml", 8.5)),
    )


def test_build_serializes_complete_report_payload() -> None:
    payload = json.loads(JsonReportBuilder.build(report=_report()))

    assert payload == {
        "candidate_level": "Senior",
        "overall_score": 8.25,
        "market_alignment_score": 0.91,
        "evaluated_questions": 6,
        "strengths": ["Python", "System design"],
        "weaknesses": ["Kubernetes depth"],
        "recommendations": ["Practice distributed tracing"],
        "category_scores": {"backend": 8.0, "ml": 8.5},
    }
