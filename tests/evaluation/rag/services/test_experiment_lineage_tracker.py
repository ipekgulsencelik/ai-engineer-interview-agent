from __future__ import annotations

import pytest

from src.evaluation.rag.services.experiment_lineage_tracker import ExperimentLineageTracker
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_tracker_should_create_append_replace_and_remove_nodes() -> None:
    tracker = ExperimentLineageTracker()
    root = experiment_node(experiment_id="root")
    child = experiment_node(experiment_id="child", parent_experiment_id="root")

    graph = tracker.create_graph(root_node=root)
    graph = tracker.append_node(graph=graph, node=child)
    graph = tracker.replace_node(graph=graph, node=experiment_node(experiment_id="child", parent_experiment_id="root", overall_score=0.9))
    graph = tracker.remove_node(graph=graph, experiment_id="child")

    assert graph.node_count == 1
    assert graph.get_node(experiment_id="child") is None


def test_experiment_lineage_tracker_should_reject_duplicate_nodes() -> None:
    tracker = ExperimentLineageTracker()
    root = experiment_node(experiment_id="root")
    graph = tracker.create_graph(root_node=root)

    with pytest.raises(ValueError):
        tracker.append_node(graph=graph, node=root)
