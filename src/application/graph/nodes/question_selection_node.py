from __future__ import annotations

from src.application.constants.mock_questions import (
    DEFAULT_QUESTION_ID,
    DEFAULT_QUESTION_TEXT,
)
from src.application.graph.nodes.base_graph_node import (
    BaseGraphNode,
)
from src.application.graph.state.interview_graph_state import (
    InterviewGraphState,
)


class QuestionSelectionNode(
    BaseGraphNode,
):
    """
    Adaptive question selection graph node.

    Bu node:
        - bir sonraki interview sorusunu belirler
        - workflow state'ini immutable-style günceller
        - future retrieval/ranking pipeline'ı için orchestration noktası sağlar
    """

    def __call__(
        self,
        state: InterviewGraphState,
    ) -> InterviewGraphState:
        return self._build_next_state(
            state=state,
        )

    @staticmethod
    def _build_next_state(
        *,
        state: InterviewGraphState,
    ) -> InterviewGraphState:
        return {
            **state,
            "current_question_id": (
                DEFAULT_QUESTION_ID
            ),
            "current_question_text": (
                DEFAULT_QUESTION_TEXT
            ),
        }