from __future__ import annotations

from src.evaluation.rag.builders.experiment_lineage_builder import ExperimentLineageBuilder
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_builder_should_create_graph_with_generated_id_and_nodes() -> None:
    root = experiment_node(experiment_id="root")
    graph = ExperimentLineageBuilder.build(root_experiment_id="root", nodes=(root,), notes="notes")

    assert graph.graph_id
    assert graph.root_experiment_id == "root"
    assert graph.nodes == (root,)
    assert graph.notes == "notes"
