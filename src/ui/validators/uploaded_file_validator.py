from __future__ import annotations

from streamlit.runtime.uploaded_file_manager import (
    UploadedFile,
)

from src.ui.validators.constants.uploaded_file_errors import (
    INVALID_PDF_FILE_ERROR,
)


class UploadedFileValidator:
    """
    Uploaded file validation utilities.
    """

    @staticmethod
    def validate_pdf_file(
        *,
        uploaded_file: UploadedFile,
    ) -> UploadedFile:
        if (
            uploaded_file.type
            != "application/pdf"
        ):
            raise ValueError(
                INVALID_PDF_FILE_ERROR,
            )

        return uploaded_file