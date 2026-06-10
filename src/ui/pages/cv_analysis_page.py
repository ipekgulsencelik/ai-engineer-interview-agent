from __future__ import annotations

import streamlit as st

from src.ui.constants.cv_page_texts import (
    CV_PAGE_TITLE,
    CV_UPLOAD_LABEL,
)
from src.ui.constants.file_upload_options import (
    PDF_FILE_TYPES,
)
from src.ui.presenters.cv_upload_presenter import (
    CVUploadPresenter,
)
from src.ui.validators.uploaded_file_validator import (
    UploadedFileValidator,
)


class CVAnalysisPage:
    """
    CV intelligence page.

    Bu sınıf:
        - CV upload page orchestration yapar
        - upload flow'unu yönetir
        - presentation ve validation detaylarını ilgili katmanlara bırakır
    """

    @staticmethod
    def render() -> None:
        st.title(
            CV_PAGE_TITLE,
        )

        uploaded_file = st.file_uploader(
            CV_UPLOAD_LABEL,
            type=PDF_FILE_TYPES,
        )

        if uploaded_file is None:
            return

        UploadedFileValidator.validate_pdf_file(
            uploaded_file=uploaded_file,
        )

        CVUploadPresenter.render_upload_success()