from __future__ import annotations

import pytest

pytest.importorskip("reportlab")

import json

from src.application.services.report_generation_service import ReportGenerationService
from src.domain.results.interview_report_result import InterviewReportResult


def _report() -> InterviewReportResult:
    return InterviewReportResult(
        candidate_level="Junior",
        overall_score=6.0,
        market_alignment_score=0.72,
        evaluated_questions=3,
        strengths=("Basics",),
        weaknesses=("Scaling",),
        recommendations=("Build production projects",),
        category_scores=(("foundations", 6.0),),
    )


def test_generate_markdown_delegates_to_markdown_builder() -> None:
    markdown = ReportGenerationService().generate_markdown(report=_report())

    assert "# AI Engineer Interview Report" in markdown
    assert "- Candidate Level: Junior" in markdown


def test_generate_json_delegates_to_json_builder() -> None:
    payload = json.loads(ReportGenerationService().generate_json(report=_report()))

    assert payload["candidate_level"] == "Junior"
    assert payload["category_scores"] == {"foundations": 6.0}


def test_generate_pdf_delegates_to_pdf_builder(tmp_path) -> None:
    output_path = tmp_path / "service-report.pdf"

    result_path = ReportGenerationService().generate_pdf(
        report=_report(),
        output_path=output_path,
    )

    assert result_path == output_path
    assert output_path.exists()
