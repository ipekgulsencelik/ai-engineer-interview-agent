from __future__ import annotations

from src.evaluation.tracking.ports.experiment_tag_metadata_store import (
    ExperimentTagMetadataStore,
)
from src.evaluation.tracking.ports.experiment_tag_query_store import (
    ExperimentTagQueryStore,
)


class ExperimentTagStore(
    ExperimentTagMetadataStore,
    ExperimentTagQueryStore,
):
    """
    Composite store port for complete experiment tag persistence.
    """

    # This class intentionally left blank. It serves as a convenient
    # interface for infrastructure adapters that support all tag store
    # operations.