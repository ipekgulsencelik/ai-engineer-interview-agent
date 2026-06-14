from __future__ import annotations

from src.evaluation.tracking.ports.experiment_lineage_graph_store import (
    ExperimentLineageGraphStore,
)
from src.evaluation.tracking.ports.experiment_node_store import (
    ExperimentNodeStore,
)
from src.evaluation.tracking.ports.experiment_run_store import (
    ExperimentRunStore,
)


class ExperimentHistoryStore(
    ExperimentRunStore,
    ExperimentNodeStore,
    ExperimentLineageGraphStore,
):
    """
    Composite store port for complete experiment history persistence.

    Use this only for infrastructure adapters that support
    run, node, and graph persistence together.
    """