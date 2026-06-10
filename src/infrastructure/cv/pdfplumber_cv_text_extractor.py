from __future__ import annotations

from pathlib import Path

import pdfplumber

from src.application.ports.cv_text_extractor import (
    CVTextExtractor,
)
from src.infrastructure.validators.cv_file_validator import (
    CVFileValidator,
)


class PdfPlumberCVTextExtractor(
    CVTextExtractor,
):
    """
    pdfplumber-based CV text extraction adapter.
    """

    def extract_text(
        self,
        *,
        file_path: str | Path,
    ) -> str:
        path = CVFileValidator.validate_pdf_file_path(
            file_path=file_path,
        )

        extracted_pages: list[str] = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text and text.strip():
                    extracted_pages.append(
                        text.strip()
                    )

        extracted_text = "\n\n".join(
            extracted_pages,
        ).strip()

        if not extracted_text:
            raise ValueError(
                "No text could be extracted from CV."
            )

        return extracted_text