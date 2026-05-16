from __future__ import annotations

from src.application.ports.question_repository import (
    QuestionRepository,
)
from src.domain.entities.question import Question


class LoadQuestionsUseCase:
    """
    Question loading orchestration use case.
    """

    def __init__(
        self,
        *,
        question_repository: QuestionRepository,
    ) -> None:
        self._question_repository = (
            question_repository
        )

    def execute(
        self,
    ) -> list[Question]:
        return (
            self._question_repository.list_all()
        )