from __future__ import annotations

import pytest

pytest.importorskip("reportlab")

from src.domain.results.interview_report_result import InterviewReportResult
from src.infrastructure.reporting.builders.pdf_report_builder import PDFReportBuilder


def test_build_writes_pdf_file(tmp_path) -> None:
    report = InterviewReportResult(
        candidate_level="Senior",
        overall_score=8.5,
        market_alignment_score=0.9,
        evaluated_questions=5,
        strengths=("Architecture",),
        weaknesses=("Cost optimization",),
        recommendations=("Study FinOps",),
        category_scores=(("system_design", 8.5),),
    )
    output_path = tmp_path / "report.pdf"

    result_path = PDFReportBuilder.build(report=report, output_path=output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    assert output_path.read_bytes().startswith(b"%PDF")
