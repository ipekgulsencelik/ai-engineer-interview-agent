from __future__ import annotations

from src.evaluation.rag.entities.experiment_lineage_graph import ExperimentLineageGraph
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_graph_should_find_root_children_and_parent() -> None:
    root = experiment_node(experiment_id="root")
    child = experiment_node(experiment_id="child", parent_experiment_id="root")
    graph = ExperimentLineageGraph(graph_id="graph-1", root_experiment_id="root", nodes=(root, child))

    assert graph.node_count == 2
    assert graph.is_empty is False
    assert graph.root_node == root
    assert graph.get_node(experiment_id="child") == child
    assert graph.get_children(experiment_id="root") == (child,)
    assert graph.get_parent(experiment_id="child") == root
