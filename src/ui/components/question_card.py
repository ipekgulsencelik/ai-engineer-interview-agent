from __future__ import annotations

import streamlit as st

from src.ui.formatters.question_response_formatter import (
    QuestionResponseFormatter,
)
from src.ui.presentation.question_metadata_item import (
    QuestionMetadataItem,
)
from src.ui.schemas.question_response import (
    QuestionResponse,
)


class QuestionCard:
    """
    Interview question display component.
    """

    @staticmethod
    def render(
        *,
        question: QuestionResponse,
    ) -> None:
        st.subheader(
            "Interview Question",
        )

        with st.container(border=True):
            QuestionCard._render_question_text(
                question=question,
            )

            st.divider()

            QuestionCard._render_metadata(
                question=question,
            )

    @staticmethod
    def _render_question_text(
        *,
        question: QuestionResponse,
    ) -> None:
        st.markdown(
            f"### {question.text}",
        )

    @staticmethod
    def _render_metadata(
        *,
        question: QuestionResponse,
    ) -> None:
        metadata_items = QuestionResponseFormatter.to_display_metadata(
            question=question,
        )

        col1, col2 = st.columns(2)

        with col1:
            QuestionCard._render_metadata_items(
                metadata_items=metadata_items[:3],
            )

        with col2:
            QuestionCard._render_metadata_items(
                metadata_items=metadata_items[3:],
            )

    @staticmethod
    def _render_metadata_items(
        *,
        metadata_items: list[QuestionMetadataItem],
    ) -> None:
        for item in metadata_items:
            QuestionCard._render_field(
                label=item.label,
                value=item.value,
            )

    @staticmethod
    def _render_field(
        *,
        label: str,
        value: str,
    ) -> None:
        st.markdown(
            f"""
            **{label}**  
            `{value}`
            """.strip(),
        )