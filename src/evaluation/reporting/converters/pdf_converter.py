from __future__ import annotations

from pathlib import Path


class PDFConverter:
    """
    Converts HTML files to PDF using WeasyPrint.
    """

    @staticmethod
    def convert(
        *,
        html_file: Path,
        pdf_file: Path,
    ) -> None:
        try:
            from weasyprint import HTML
        except ImportError as exc:
            raise RuntimeError(
                "PDF export requires WeasyPrint. "
                "Install it with `pip install weasyprint`."
            ) from exc

        HTML(
            filename=str(
                html_file,
            )
        ).write_pdf(
            str(
                pdf_file,
            )
        )