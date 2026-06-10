from __future__ import annotations

import streamlit as st


class NotificationRenderer:
    """
    Reusable notification rendering helper.
    """

    @staticmethod
    def render_success(
        *,
        message: str,
    ) -> None:
        st.success(
            message,
        )

    @staticmethod
    def render_info(
        *,
        message: str,
    ) -> None:
        st.info(
            message,
        )