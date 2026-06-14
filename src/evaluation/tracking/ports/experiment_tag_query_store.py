from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.tracking.entities.experiment_tag import (
    ExperimentTag,
)


class ExperimentTagQueryStore(
    ABC,
):
    """
    Store port for experiment tag querying.
    """

    @abstractmethod
    def get_by_id(
        self,
        *,
        tag_id: str,
    ) -> ExperimentTag | None:
        """
        Returns tag by id.
        """

    @abstractmethod
    def get_by_key_value(
        self,
        *,
        key: str,
        value: str,
    ) -> ExperimentTag | None:
        """
        Returns tag by key-value pair.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> tuple[
        ExperimentTag,
        ...,
    ]:
        """
        Lists all tags.
        """

    @abstractmethod
    def list_by_key(
        self,
        *,
        key: str,
    ) -> tuple[
        ExperimentTag,
        ...,
    ]:
        """
        Lists tags by key.
        """

    @abstractmethod
    def list_by_namespace(
        self,
        *,
        namespace: str,
    ) -> tuple[
        ExperimentTag,
        ...,
    ]:
        """
        Lists tags by key namespace.
        """

    @abstractmethod
    def exists_key_value(
        self,
        *,
        key: str,
        value: str,
    ) -> bool:
        """
        Returns whether key-value tag exists.
        """