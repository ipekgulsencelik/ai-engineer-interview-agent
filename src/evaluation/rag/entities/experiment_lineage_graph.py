from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.ops.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.ops.validators.experiment_lineage_graph_validator import (
    ExperimentLineageGraphValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentLineageGraph:
    """
    Immutable experiment lineage graph.

    Represents a directed acyclic graph (DAG)
    of experiment evolution.

    Each node corresponds to a specific
    experiment version and may reference
    a parent experiment.
    """

    graph_id: str

    root_experiment_id: str

    nodes: tuple[
        ExperimentNode,
        ...,
    ]

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentLineageGraphValidator.validate(
            graph_id=self.graph_id,
            root_experiment_id=(
                self.root_experiment_id
            ),
            nodes=self.nodes,
            notes=self.notes,
        )

    @property
    def node_count(
        self,
    ) -> int:
        return len(
            self.nodes,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return (
            len(
                self.nodes,
            )
            == 0
        )

    @property
    def root_node(
        self,
    ) -> ExperimentNode | None:
        for node in self.nodes:
            if (
                node.experiment_id
                == self.root_experiment_id
            ):
                return node

        return None

    def get_node(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentNode | None:
        for node in self.nodes:
            if (
                node.experiment_id
                == experiment_id
            ):
                return node

        return None

    def get_children(
        self,
        *,
        experiment_id: str,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        return tuple(
            node
            for node in self.nodes
            if (
                node.parent_experiment_id
                == experiment_id
            )
        )

    def get_parent(
        self,
        *,
        experiment_id: str,
    ) -> ExperimentNode | None:
        node = self.get_node(
            experiment_id=experiment_id,
        )

        if (
            node is None
            or node.parent_experiment_id
            is None
        ):
            return None

        return self.get_node(
            experiment_id=(
                node.parent_experiment_id
            ),
        )

    def has_node(
        self,
        *,
        experiment_id: str,
    ) -> bool:
        return (
            self.get_node(
                experiment_id=experiment_id,
            )
            is not None
        )

    def has_root(
        self,
    ) -> bool:
        return (
            self.root_node
            is not None
        )