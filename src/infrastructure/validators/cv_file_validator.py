from __future__ import annotations

from pathlib import Path


class CVFileValidator:
    """
    CV file path validation helper.
    """

    @staticmethod
    def validate_pdf_file_path(
        *,
        file_path: str | Path,
    ) -> Path:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"CV file not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"CV path must be a file: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"CV file must be a PDF: {path}"
            )

        return path