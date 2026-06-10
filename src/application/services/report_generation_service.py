from __future__ import annotations

from pathlib import Path

from src.infrastructure.reporting.builders.json_report_builder import (
    JsonReportBuilder,
)
from src.infrastructure.reporting.builders.markdown_report_builder import (
    MarkdownReportBuilder,
)
from src.infrastructure.reporting.builders.pdf_report_builder import (
    PDFReportBuilder,
)
from src.domain.results.interview_report_result import (
    InterviewReportResult,
)


class ReportGenerationService:
    """
    Multi-format report generation orchestration.
    """

    def generate_markdown(
        self,
        *,
        report: InterviewReportResult,
    ) -> str:
        return MarkdownReportBuilder.build(
            report=report,
        )

    def generate_json(
        self,
        *,
        report: InterviewReportResult,
    ) -> str:
        return JsonReportBuilder.build(
            report=report,
        )

    def generate_pdf(
        self,
        *,
        report: InterviewReportResult,
        output_path: str | Path,
    ) -> Path:
        return PDFReportBuilder.build(
            report=report,
            output_path=output_path,
        )