from __future__ import annotations

from typing import Any, Mapping

from src.domain.entities.question import Question
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.validators.question_record_validator import QuestionRecordValidator
from src.infrastructure.mappers.question_mapper import QuestionMapper
from src.infrastructure.repositories.question_bank_loader import QuestionBankLoader
from src.infrastructure.validators.question_collection_validator import (
    QuestionCollectionValidator,
)
from src.infrastructure.validators.question_lookup_validator import (
    QuestionLookupValidator,
)
from src.infrastructure.validators.question_repository_config_validator import (
    QuestionRepositoryConfigValidator,
)


class JsonQuestionRepository(QuestionRepository):
    """JSON-backed implementation of the QuestionRepository contract."""

    def __init__(self, file_path: str | Path) -> None:
        QuestionRepositoryConfigValidator.validate_file_path(file_path)

        resolved_path = Path(file_path)
        self.file_path = resolved_path
        self._loader = QuestionBankLoader(resolved_path)


    def list_all(self) -> list[Question]:
        raw_items = self._loader.load_items()
        questions = [
            self._build_question(
                item=item,
                index=index,
            )
            for index, item in enumerate(raw_items)
        ]

        QuestionCollectionValidator.validate_unique_ids(questions)

        return questions

    def get_by_id(self, question_id: str) -> Question | None:
        QuestionLookupValidator.validate_question_id(question_id)

        for question in self.list_all():
            if question.id == question_id:
                return question

        return None

    def exists(self) -> bool:
        return self._loader.exists()

    @staticmethod
    def _build_question(item: Mapping[str, Any], index: int) -> Question:
        QuestionRecordValidator.validate(item=item, index=index)

        return QuestionMapper.from_mapping(payload=item, index=index)