from __future__ import annotations

from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import Flowable

from src.infrastructure.constants.pdf_report import (
    PDF_REPORT_TITLE,
)
from src.infrastructure.reporting.factories.pdf_report_element_factory import (
    PDFReportElementFactory,
)
from src.domain.results.interview_report_result import (
    InterviewReportResult,
)


class PDFReportBuilder:
    """
    PDF interview report builder.
    """

    @staticmethod
    def build(
        *,
        report: InterviewReportResult,
        output_path: str | Path,
    ) -> Path:
        path = Path(
            output_path,
        )

        document = SimpleDocTemplate(
            str(path),
        )

        styles = getSampleStyleSheet()

        elements: list[Flowable] = [
            PDFReportElementFactory.title(
                text=PDF_REPORT_TITLE,
                styles=styles,
            ),
            PDFReportElementFactory.small_spacer(),
            PDFReportElementFactory.label_value(
                label="Candidate Level",
                value=report.candidate_level,
                styles=styles,
            ),
            PDFReportElementFactory.label_value(
                label="Overall Score",
                value=f"{report.overall_score:.2f}/10",
                styles=styles,
            ),
            PDFReportElementFactory.label_value(
                label="Market Alignment",
                value=f"{report.market_alignment_score:.2f}",
                styles=styles,
            ),
            PDFReportElementFactory.label_value(
                label="Evaluated Questions",
                value=str(report.evaluated_questions),
                styles=styles,
            ),
            PDFReportElementFactory.section_spacer(),
            PDFReportElementFactory.heading(
                text="Strengths",
                styles=styles,
            ),
        ]

        for item in report.strengths:
            elements.append(
                PDFReportElementFactory.bullet(
                    text=item,
                    styles=styles,
                )
            )

        elements.append(
            PDFReportElementFactory.section_spacer()
        )

        elements.append(
            PDFReportElementFactory.heading(
                text="Weaknesses",
                styles=styles,
            )
        )

        for item in report.weaknesses:
            elements.append(
                PDFReportElementFactory.bullet(
                    text=item,
                    styles=styles,
                )
            )

        elements.append(
            PDFReportElementFactory.section_spacer()
        )

        elements.append(
            PDFReportElementFactory.heading(
                text="Recommendations",
                styles=styles,
            )
        )

        for item in report.recommendations:
            elements.append(
                PDFReportElementFactory.bullet(
                    text=item,
                    styles=styles,
                )
            )

        document.build(
            elements,
        )

        return path