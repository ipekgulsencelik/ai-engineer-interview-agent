from __future__ import annotations

import pytest

from src.evaluation.rag.validators.experiment_lineage_validator import (
    ExperimentLineageValidator,
)
from tests.evaluation.rag.factories import experiment_node


def test_experiment_lineage_validator_should_validate_unique_nodes_without_graph_dependency() -> None:
    ExperimentLineageValidator.validate_unique_nodes(
        nodes=(
            experiment_node(experiment_id="root"),
            experiment_node(experiment_id="child", parent_experiment_id="root"),
        )
    )


def test_experiment_lineage_validator_should_reject_duplicate_nodes_without_tracker_logic() -> None:
    with pytest.raises(ValueError):
        ExperimentLineageValidator.validate_unique_nodes(
            nodes=(
                experiment_node(experiment_id="root"),
                experiment_node(experiment_id="root"),
            )
        )
