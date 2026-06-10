from __future__ import annotations

from src.application.graph.nodes.base_graph_node import (
    BaseGraphNode,
)
from src.application.constants.mock_followups import (
    DEFAULT_FOLLOW_UP_QUESTION,
)
from src.application.graph.state.interview_graph_state import (
    InterviewGraphState,
)


class FollowupGenerationNode(
    BaseGraphNode,
):
    """
    Dynamic follow-up generation node.
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
            "follow_up_question": (
                DEFAULT_FOLLOW_UP_QUESTION
            ),
        }