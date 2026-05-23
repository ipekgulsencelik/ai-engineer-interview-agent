from __future__ import annotations

import streamlit as st


class SectionRenderer:
    """
    Reusable UI section rendering helper.
    """

    @staticmethod
    def render(
        *,
        title: str,
        content: object,
    ) -> None:
        st.subheader(
            title,
        )

        st.write(
            content,
        )