from __future__ import annotations

from src.ui.components.score_cards import (
    ScoreCards,
)
from src.ui.constants.evaluation_section_titles import (
    FEEDBACK_SECTION_TITLE,
    FOLLOW_UP_QUESTION_SECTION_TITLE,
    MISSING_KEYWORDS_SECTION_TITLE,
)
from src.ui.presenters.helpers.section_renderer import (
    SectionRenderer,
)
from src.ui.schemas.evaluation_response import (
    EvaluationResponse,
)


class EvaluationPresenter:
    """
    Evaluation result presenter.
    """

    @staticmethod
    def render(
        *,
        evaluation: EvaluationResponse,
    ) -> None:
        ScoreCards.render(
            evaluation=evaluation,
        )

        SectionRenderer.render(
            title=FEEDBACK_SECTION_TITLE,
            content=evaluation.feedback,
        )

        SectionRenderer.render(
            title=MISSING_KEYWORDS_SECTION_TITLE,
            content=evaluation.missing_keywords,
        )

        EvaluationPresenter._render_follow_up_question(
            evaluation=evaluation,
        )

    @staticmethod
    def _render_follow_up_question(
        *,
        evaluation: EvaluationResponse,
    ) -> None:
        if not evaluation.follow_up_question:
            return

        SectionRenderer.render(
            title=FOLLOW_UP_QUESTION_SECTION_TITLE,
            content=evaluation.follow_up_question,
        )