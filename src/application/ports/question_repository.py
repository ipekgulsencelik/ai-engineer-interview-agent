from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.entities.question import Question


class QuestionRepository(ABC):
    """
    Question repository contract.
    """

    @abstractmethod
    def list_all(self) -> list[Question]:
        """
        Return all available questions.
        """

    @abstractmethod
    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """
        Return question by id if exists.
        """

    @abstractmethod
    def exists(self) -> bool:
        """
        Return whether underlying repository source exists.
        """