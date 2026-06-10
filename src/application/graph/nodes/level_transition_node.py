from __future__ import annotations

from src.application.graph.nodes.base_graph_node import (
    BaseGraphNode,
)
from src.application.constants.level_transition import (
    JUNIOR_LEVEL,
    JUNIOR_THRESHOLD,
    MID_LEVEL,
    SENIOR_LEVEL,
    SENIOR_THRESHOLD,
)
from src.application.graph.state.interview_graph_state import (
    InterviewGraphState,
)


class LevelTransitionNode(
    BaseGraphNode,
):
    """
    Adaptive level transition node.
    """

    def __call__(
        self,
        state: InterviewGraphState,
    ) -> InterviewGraphState:
        next_level = self._determine_next_level(
            state=state,
        )

        return {
            **state,
            "current_level": next_level,
        }

    @staticmethod
    def _determine_next_level(
        *,
        state: InterviewGraphState,
    ) -> str:
        score = float(
            state.get(
                "evaluation_score",
                0.0,
            )
        )

        if score >= SENIOR_THRESHOLD:
            return SENIOR_LEVEL

        if score <= JUNIOR_THRESHOLD:
            return JUNIOR_LEVEL

        return MID_LEVEL