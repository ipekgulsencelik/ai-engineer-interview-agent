from __future__ import annotations

from src.evaluation.rag.entities.experiment_lineage_graph import ExperimentLineageGraph
from src.evaluation.rag.traversers.experiment_lineage_traverser import ExperimentLineageTraverser
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_traverser_should_return_ancestors_descendants_and_path_to_root() -> None:
    root = experiment_node(experiment_id="root")
    child = experiment_node(experiment_id="child", parent_experiment_id="root")
    grandchild = experiment_node(experiment_id="grandchild", parent_experiment_id="child")
    graph = ExperimentLineageGraph(graph_id="graph-1", root_experiment_id="root", nodes=(root, child, grandchild))

    assert ExperimentLineageTraverser.ancestors(graph=graph, experiment_id="grandchild") == (child, root)
    assert set(ExperimentLineageTraverser.descendants(graph=graph, experiment_id="root")) == {child, grandchild}
    assert ExperimentLineageTraverser.path_to_root(graph=graph, experiment_id="grandchild") == (grandchild, child, root)
