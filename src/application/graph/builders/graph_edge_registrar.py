from __future__ import annotations

from langgraph.graph import END
from langgraph.graph import StateGraph

from src.application.constants.graph_nodes import (
    EVALUATION_NODE,
    FOLLOWUP_GENERATION_NODE,
    LEVEL_TRANSITION_NODE,
    QUESTION_SELECTION_NODE,
)


class GraphEdgeRegistrar:
    """
    LangGraph edge registration helper.
    """

    @staticmethod
    def register(
        *,
        graph: StateGraph,
    ) -> None:
        edges = (
            (
                QUESTION_SELECTION_NODE,
                EVALUATION_NODE,
            ),
            (
                EVALUATION_NODE,
                LEVEL_TRANSITION_NODE,
            ),
            (
                LEVEL_TRANSITION_NODE,
                FOLLOWUP_GENERATION_NODE,
            ),
            (
                FOLLOWUP_GENERATION_NODE,
                END,
            ),
        )

        for start_node, end_node in edges:
            graph.add_edge(
                start_node,
                end_node,
            )