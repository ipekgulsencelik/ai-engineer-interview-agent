from __future__ import annotations

from pathlib import Path

from src.evaluation.ops.exporters.pdf_converter import (
    PDFConverter,
)
from src.evaluation.ops.exporters.temporary_html_file_factory import (
    TemporaryHTMLFileFactory,
)


class PDFWriter:
    """
    Writes HTML content as PDF.
    """

    def __init__(
        self,
        *,
        converter: PDFConverter | None = None,
        html_factory: (
            TemporaryHTMLFileFactory | None
        ) = None,
    ) -> None:
        self._converter = (
            converter
            or PDFConverter()
        )

        self._html_factory = (
            html_factory
            or TemporaryHTMLFileFactory()
        )

    def write(
        self,
        *,
        html: str,
        output_path: str | Path,
    ) -> Path:
        pdf_path = Path(
            output_path,
        )

        pdf_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_html_path = (
            self._html_factory.create(
                html=html,
            )
        )

        try:
            self._converter.convert(
                html_file=temporary_html_path,
                pdf_file=pdf_path,
            )
        finally:
            temporary_html_path.unlink(
                missing_ok=True,
            )

        return pdf_path