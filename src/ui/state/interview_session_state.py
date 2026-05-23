from __future__ import annotations

import streamlit as st

from src.ui.schemas.question_response import (
    QuestionResponse,
)
from src.ui.constants.session_state_keys import (
    CURRENT_QUESTION_KEY,
)
from src.ui.validators.session_state_validator import (
    SessionStateValidator,
)


class InterviewSessionState:
    """
    Interview page session state manager.

    Bu sınıf:
        - Streamlit session_state erişimini merkezi hale getirir
        - current question lifecycle'ını yönetir
        - page katmanını state implementation detaylarından izole eder
    """

    @staticmethod
    def set_current_question(
        *,
        question: QuestionResponse,
    ) -> None:
        st.session_state[
            CURRENT_QUESTION_KEY
        ] = question

    @staticmethod
    def get_current_question() -> QuestionResponse | None:
        value = st.session_state.get(
            CURRENT_QUESTION_KEY,
        )

        if value is None:
            return None

        return SessionStateValidator.validate_question_response(
            value=value,
        )

    @staticmethod
    def has_current_question() -> bool:
        return (
            CURRENT_QUESTION_KEY
            in st.session_state
        )

    @staticmethod
    def clear_current_question() -> None:
        st.session_state.pop(
            CURRENT_QUESTION_KEY,
            None,
        )