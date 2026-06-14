from __future__ import annotations

import pytest

pytest.importorskip("reportlab")

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer

from src.infrastructure.constants.pdf_report import (
    PDF_SECTION_SPACER_HEIGHT,
    PDF_SMALL_SPACER_HEIGHT,
    PDF_SPACER_WIDTH,
)
from src.infrastructure.reporting.factories.pdf_report_element_factory import PDFReportElementFactory


def test_factory_creates_paragraph_elements() -> None:
    styles = getSampleStyleSheet()

    assert isinstance(PDFReportElementFactory.title(text="Title", styles=styles), Paragraph)
    assert isinstance(PDFReportElementFactory.heading(text="Heading", styles=styles), Paragraph)
    assert isinstance(PDFReportElementFactory.paragraph(text="Body", styles=styles), Paragraph)
    assert isinstance(
        PDFReportElementFactory.label_value(label="Score", value="9", styles=styles),
        Paragraph,
    )
    assert isinstance(PDFReportElementFactory.bullet(text="Item", styles=styles), Paragraph)


def test_factory_creates_configured_spacers() -> None:
    small = PDFReportElementFactory.small_spacer()
    section = PDFReportElementFactory.section_spacer()

    assert isinstance(small, Spacer)
    assert small.width == PDF_SPACER_WIDTH
    assert small.height == PDF_SMALL_SPACER_HEIGHT
    assert isinstance(section, Spacer)
    assert section.width == PDF_SPACER_WIDTH
    assert section.height == PDF_SECTION_SPACER_HEIGHT
