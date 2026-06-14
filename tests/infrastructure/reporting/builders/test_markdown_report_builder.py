from __future__ import annotations

from src.domain.results.interview_report_result import InterviewReportResult
from src.infrastructure.reporting.builders.markdown_report_builder import MarkdownReportBuilder


def test_build_renders_summary_and_sections() -> None:
    report = InterviewReportResult(
        candidate_level="Mid",
        overall_score=7.125,
        market_alignment_score=0.84,
        evaluated_questions=4,
        strengths=("Clean Python",),
        weaknesses=("Needs cloud depth",),
        recommendations=("Review RAG evaluation", "Practice observability"),
        category_scores=(("python", 7.0),),
    )

    markdown = MarkdownReportBuilder.build(report=report)

    assert markdown.startswith("# AI Engineer Interview Report")
    assert "- Candidate Level: Mid" in markdown
    assert "- Overall Score: 7.12/10" in markdown
    assert "- Market Alignment: 0.84" in markdown
    assert "- Evaluated Questions: 4" in markdown
    assert "## Strengths" in markdown
    assert "- Clean Python" in markdown
    assert "## Weaknesses" in markdown
    assert "- Needs cloud depth" in markdown
    assert "## Recommendations" in markdown
    assert "- Review RAG evaluation" in markdown
    assert "- Practice observability" in markdown
