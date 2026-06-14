from __future__ import annotations

from src.evaluation.tracking.repositories.experiment_command_repository import (
    ExperimentCommandRepository,
)
from src.evaluation.tracking.repositories.experiment_query_repository import (
    ExperimentQueryRepository,
)
from src.evaluation.tracking.repositories.experiment_search_repository import (
    ExperimentSearchRepository,
)


class ExperimentRepository(
    ExperimentCommandRepository,
    ExperimentQueryRepository,
    ExperimentSearchRepository,
):
    """
    Composite repository for experiment metadata.
    """

    # This class intentionally left blank. It serves as a convenient
    # interface for repositories that need to support commands, queries,
    # and search operations together.