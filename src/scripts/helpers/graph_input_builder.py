from __future__ import annotations

from src.application.graph.state.interview_graph_state import (
    InterviewGraphState,
)
from src.scripts.constants.mock_graph_input import (
    DEFAULT_CANDIDATE_ANSWER,
    DEFAULT_LEVEL,
    DEFAULT_QUERY,
    DEFAULT_TARGET_DIFFICULTY,
)


class GraphInputBuilder:
    """
    Graph input payload builder.
    """

    @staticmethod
    def build() -> InterviewGraphState:
        return {
            "query": DEFAULT_QUERY,
            "candidate_answer": (
                DEFAULT_CANDIDATE_ANSWER
            ),
            "current_level": DEFAULT_LEVEL,
            "target_difficulty": (
                DEFAULT_TARGET_DIFFICULTY
            ),
        }