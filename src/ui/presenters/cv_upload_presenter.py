from __future__ import annotations

from src.ui.constants.cv_page_texts import (
    CV_PENDING_INTEGRATION_MESSAGE,
    CV_UPLOAD_SUCCESS_MESSAGE,
)
from src.ui.presenters.helpers.notification_renderer import (
    NotificationRenderer,
)


class CVUploadPresenter:
    """
    CV upload presentation helper.
    """

    @staticmethod
    def render_upload_success() -> None:
        NotificationRenderer.render_success(
            message=CV_UPLOAD_SUCCESS_MESSAGE,
        )

        NotificationRenderer.render_info(
            message=CV_PENDING_INTEGRATION_MESSAGE,
        )