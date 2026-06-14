from __future__ import annotations

import pytest

from tests.evaluation.rag.factories import experiment_node


def test_experiment_node_should_expose_root_parent_and_success_rate_properties() -> None:
    node = experiment_node(parent_experiment_id=None, pass_rate=0.75)
    assert node.is_root is True
    assert node.has_parent is False
    assert node.success_rate == 0.75


def test_experiment_node_should_reject_empty_experiment_id() -> None:
    with pytest.raises(ValueError):
        experiment_node(experiment_id="")
