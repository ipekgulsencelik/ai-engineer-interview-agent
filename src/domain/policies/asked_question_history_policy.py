from __future__ import annotations

from src.domain.constants.interview_session import (
    MAX_ASKED_QUESTION_HISTORY,
)


class AskedQuestionHistoryPolicy:
    """
    Asked question history update policy.
    """

    @staticmethod
    def append_question_id(
        *,
        asked_question_ids: tuple[str, ...],
        question_id: str,
    ) -> tuple[str, ...]:
        updated_question_ids = (
            asked_question_ids
            + (question_id,)
        )

        return updated_question_ids[
            -MAX_ASKED_QUESTION_HISTORY:
        ]