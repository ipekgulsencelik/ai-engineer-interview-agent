from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_tag import (
    ExperimentTag,
)


class ExperimentTagMetadataStore(
    ABC,
):
    """
    Store port for experiment tag metadata persistence.
    """

    @abstractmethod
    def save(
        self,
        *,
        tag: ExperimentTag,
    ) -> None:
        """
        Persists an experiment tag.
        """

    @abstractmethod
    def exists(
        self,
        *,
        tag_id: str,
    ) -> bool:
        """
        Returns whether tag exists by id.
        """

    @abstractmethod
    def delete(
        self,
        *,
        tag_id: str,
    ) -> None:
        """
        Deletes tag by id.
        """