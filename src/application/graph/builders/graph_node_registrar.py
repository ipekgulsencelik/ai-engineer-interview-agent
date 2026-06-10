from __future__ import annotations

from langgraph.graph import StateGraph

from src.application.constants.graph_nodes import (
    EVALUATION_NODE,
    FOLLOWUP_GENERATION_NODE,
    LEVEL_TRANSITION_NODE,
    QUESTION_SELECTION_NODE,
)
from src.application.graph.nodes.evaluation_node import (
    EvaluationNode,
)
from src.application.graph.nodes.followup_generation_node import (
    FollowupGenerationNode,
)
from src.application.graph.nodes.level_transition_node import (
    LevelTransitionNode,
)
from src.application.graph.nodes.question_selection_node import (
    QuestionSelectionNode,
)


class GraphNodeRegistrar:
    """
    LangGraph node registration helper.
    """

    @staticmethod
    def register(
        *,
        graph: StateGraph,
    ) -> None:
        nodes = (
            (
                QUESTION_SELECTION_NODE,
                QuestionSelectionNode(),
            ),
            (
                EVALUATION_NODE,
                EvaluationNode(),
            ),
            (
                LEVEL_TRANSITION_NODE,
                LevelTransitionNode(),
            ),
            (
                FOLLOWUP_GENERATION_NODE,
                FollowupGenerationNode(),
            ),
        )

        for node_name, node in nodes:
            graph.add_node(
                node_name,
                node,
            )