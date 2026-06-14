from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_node import (
    ExperimentNode,
)
from src.evaluation.tracking.value_objects.experiment_query import (
    ExperimentQuery,
)


class ExperimentSearchRepository(
    ABC,
):
    """
    Repository port for structured experiment search.
    """

    @abstractmethod
    def search(
        self,
        *,
        query: ExperimentQuery,
    ) -> tuple[
        ExperimentNode,
        ...,
    ]:
        """
        Searches experiments using structured criteria.
        """