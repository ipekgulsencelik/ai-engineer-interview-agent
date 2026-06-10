from __future__ import annotations

from src.application.constants.mock_evaluation import (
    DEFAULT_EVALUATION_SCORE,
    DEFAULT_FEEDBACK_TEXT,
)
from src.application.graph.interview_graph_state import (
    InterviewGraphState,
)
from src.application.graph.nodes.base_graph_node import (
    BaseGraphNode,
)


class EvaluationNode(BaseGraphNode):
    """
    Candidate answer evaluation graph node.

    Bu node:
        - candidate answer evaluation orchestration yapar
        - evaluation sonucunu workflow state'ine yazar
        - future evaluator service integration'ı için entry point sağlar
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
            "evaluation_score": (
                DEFAULT_EVALUATION_SCORE
            ),
            "feedback": (
                DEFAULT_FEEDBACK_TEXT
            ),
        }