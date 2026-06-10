from __future__ import annotations

import streamlit as st

from src.ui.components.question_card import (
    QuestionCard,
)
from src.ui.constants.interview_defaults import (
    DEFAULT_INTERVIEW_TOPIC,
)
from src.ui.factories.evaluation_response_factory import (
    EvaluationResponseFactory,
)
from src.ui.factories.question_response_factory import (
    QuestionResponseFactory,
)
from src.ui.presenters.evaluation_presenter import (
    EvaluationPresenter,
)
from src.ui.schemas.question_response import (
    QuestionResponse,
)
from src.ui.services.api_client import (
    APIClient,
)
from src.ui.state.interview_session_state import (
    InterviewSessionState,
)


class InterviewPage:
    """
    Interactive AI interview page.

    Bu sınıf:
        - page flow orchestration yapar
        - user inputlarını toplar
        - API çağrılarını tetikler
        - state/presentation/component detaylarını ilgili katmanlara bırakır
    """

    @staticmethod
    def render() -> None:
        st.title(
            "AI Engineer Interview",
        )

        query = InterviewPage._render_topic_input()

        InterviewPage._handle_question_generation(
            query=query,
        )

        InterviewPage._render_current_question_section()

    @staticmethod
    def _render_topic_input() -> str:
        return st.text_input(
            "Interview Topic",
            value=DEFAULT_INTERVIEW_TOPIC,
        )

    @staticmethod
    def _handle_question_generation(
        *,
        query: str,
    ) -> None:
        if not st.button(
            "Generate Question",
        ):
            return

        question_payload = APIClient.get_next_question(
            query=query,
        )

        question = QuestionResponseFactory.create(
            payload=question_payload,
        )

        InterviewSessionState.set_current_question(
            question=question,
        )

    @staticmethod
    def _render_current_question_section() -> None:
        question = InterviewSessionState.get_current_question()

        if question is None:
            return

        QuestionCard.render(
            question=question,
        )

        answer = InterviewPage._render_answer_input()

        InterviewPage._handle_answer_evaluation(
            question=question,
            answer=answer,
        )

    @staticmethod
    def _render_answer_input() -> str:
        return st.text_area(
            "Your Answer",
            height=220,
        )

    @staticmethod
    def _handle_answer_evaluation(
        *,
        question: QuestionResponse,
        answer: str,
    ) -> None:
        if not st.button(
            "Evaluate Answer",
        ):
            return

        evaluation_payload = APIClient.evaluate_answer(
            question_id=question.id,
            answer=answer,
        )

        evaluation = EvaluationResponseFactory.create(
            payload=evaluation_payload,
        )

        EvaluationPresenter.render(
            evaluation=evaluation,
        )