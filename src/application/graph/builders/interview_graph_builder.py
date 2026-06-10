from __future__ import annotations

from langgraph.graph import CompiledGraph
from langgraph.graph import StateGraph

from src.application.graph.builders.graph_edge_registrar import (
    GraphEdgeRegistrar,
)
from src.application.graph.builders.graph_node_registrar import (
    GraphNodeRegistrar,
)
from src.application.constants.graph_nodes import (
    QUESTION_SELECTION_NODE,
)
from src.application.graph.state.interview_graph_state import (
    InterviewGraphState,
)


class InterviewGraphBuilder:
    """
    LangGraph interview workflow builder.
    """

    @staticmethod
    def build() -> CompiledGraph:
        graph = StateGraph(
            InterviewGraphState,
        )

        GraphNodeRegistrar.register(
            graph=graph,
        )

        GraphEdgeRegistrar.register(
            graph=graph,
        )

        graph.set_entry_point(
            QUESTION_SELECTION_NODE,
        )

        return graph.compile()