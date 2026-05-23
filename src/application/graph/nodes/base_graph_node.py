from __future__ import annotations

from abc import ABC, abstractmethod

from src.application.graph.interview_graph_state import (
    InterviewGraphState,
)


class BaseGraphNode(ABC):
    """
    Base contract for LangGraph workflow nodes.
    """

    @abstractmethod
    def __call__(
        self,
        state: InterviewGraphState,
    ) -> InterviewGraphState:
        """
        Execute node transition.
        """