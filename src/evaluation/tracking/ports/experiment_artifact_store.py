from __future__ import annotations

from src.evaluation.tracking.ports.experiment_artifact_content_store import (
    ExperimentArtifactContentStore,
)
from src.evaluation.tracking.ports.experiment_artifact_metadata_store import (
    ExperimentArtifactMetadataStore,
)
from src.evaluation.tracking.ports.experiment_artifact_query_store import (
    ExperimentArtifactQueryStore,
)


class ExperimentArtifactStore(
    ExperimentArtifactMetadataStore,
    ExperimentArtifactContentStore,
    ExperimentArtifactQueryStore,
):
    """
    Composite artifact store.
    """

    # This class intentionally left blank. It serves as a convenient
    # interface for infrastructure adapters that support all artifact
    # store operations.