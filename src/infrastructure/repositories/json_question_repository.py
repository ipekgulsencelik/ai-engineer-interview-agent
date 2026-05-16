from __future__ import annotations

from typing import Any, Mapping

from src.application.ports.question_repository import (
    QuestionRepository,
)
from src.domain.entities.question import Question
from src.infrastructure.loaders.question_bank_loader import (
    QuestionBankLoader,
)
from src.infrastructure.mappers.question_mapper import (
    QuestionMapper,
)
from src.infrastructure.validators.question_collection_validator import (
    QuestionCollectionValidator,
)
from src.infrastructure.validators.question_lookup_validator import (
    QuestionLookupValidator,
)


class JsonQuestionRepository(QuestionRepository):
    """
    JSON-backed QuestionRepository implementation.

    Bu sınıf:
        - repository contract'ını implemente eder
        - loader, mapper ve validator bileşenlerini orkestre eder

    Concrete dependency oluşturmaz.
    """

    def __init__(
        self,
        *,
        loader: QuestionBankLoader,
        mapper: QuestionMapper,
    ) -> None:
        self._loader = loader
        self._mapper = mapper

    def list_all(self) -> list[Question]:
        raw_items = self._loader.load_items()

        questions = [
            self._map_question(
                item=item,
                index=index,
            )
            for index, item in enumerate(raw_items)
        ]

        QuestionCollectionValidator.validate_unique_ids(
            questions,
        )

        return questions

    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        QuestionLookupValidator.validate_question_id(
            question_id,
        )

        return next(
            (
                question
                for question in self.list_all()
                if question.id == question_id
            ),
            None,
        )

    def exists(self) -> bool:
        return self._loader.exists()

    def _map_question(
        self,
        *,
        item: Mapping[str, Any],
        index: int,
    ) -> Question:
        return self._mapper.from_mapping(
            payload=item,
            index=index,
        )