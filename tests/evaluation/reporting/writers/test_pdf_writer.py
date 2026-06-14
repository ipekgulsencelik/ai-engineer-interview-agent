from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.writers.pdf_writer import PDFWriter


class FakeHTMLFactory:
    def __init__(self, path: Path) -> None:
        self.path = path

    def create(self, *, html: str) -> Path:
        self.path.write_text(html, encoding="utf-8")
        return self.path


class FakeConverter:
    def __init__(self) -> None:
        self.html_file: Path | None = None
        self.pdf_file: Path | None = None

    def convert(self, *, html_file: Path, pdf_file: Path) -> None:
        self.html_file = html_file
        self.pdf_file = pdf_file
        pdf_file.write_bytes(b"%PDF fake")


def test_write_uses_converter_and_removes_temporary_html(tmp_path) -> None:
    temporary_html = tmp_path / "temporary.html"
    output_path = tmp_path / "nested" / "report.pdf"
    converter = FakeConverter()

    result = PDFWriter(
        converter=converter,
        html_factory=FakeHTMLFactory(path=temporary_html),
    ).write(html="<h1>PDF</h1>", output_path=output_path)

    assert result == output_path
    assert output_path.read_bytes() == b"%PDF fake"
    assert converter.html_file == temporary_html
    assert converter.pdf_file == output_path
    assert not temporary_html.exists()
