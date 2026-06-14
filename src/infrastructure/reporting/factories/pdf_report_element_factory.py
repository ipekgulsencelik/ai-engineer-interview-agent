from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus.flowables import Flowable

from src.infrastructure.constants.pdf_report import (
    PDF_SECTION_SPACER_HEIGHT,
    PDF_SMALL_SPACER_HEIGHT,
    PDF_SPACER_WIDTH,
)


class PDFReportElementFactory:
    """
    ReportLab PDF element factory.
    """

    @staticmethod
    def title(
        *,
        text: str,
        styles: StyleSheet1,
    ) -> Flowable:
        return Paragraph(
            text,
            styles["Title"],
        )

    @staticmethod
    def heading(
        *,
        text: str,
        styles: StyleSheet1,
    ) -> Flowable:
        return Paragraph(
            f"<b>{text}</b>",
            styles["Heading2"],
        )

    @staticmethod
    def paragraph(
        *,
        text: str,
        styles: StyleSheet1,
    ) -> Flowable:
        return Paragraph(
            text,
            styles["BodyText"],
        )

    @staticmethod
    def label_value(
        *,
        label: str,
        value: str,
        styles: StyleSheet1,
    ) -> Flowable:
        return Paragraph(
            f"<b>{label}:</b> {value}",
            styles["BodyText"],
        )

    @staticmethod
    def bullet(
        *,
        text: str,
        styles: StyleSheet1,
    ) -> Flowable:
        return Paragraph(
            f"• {text}",
            styles["BodyText"],
        )

    @staticmethod
    def small_spacer() -> Flowable:
        return Spacer(
            PDF_SPACER_WIDTH,
            PDF_SMALL_SPACER_HEIGHT,
        )

    @staticmethod
    def section_spacer() -> Flowable:
        return Spacer(
            PDF_SPACER_WIDTH,
            PDF_SECTION_SPACER_HEIGHT,
        )