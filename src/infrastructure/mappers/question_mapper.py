from __future__ import annotations

from typing import Any, Mapping

from src.domain.entities.question import Question
from src.application.factories.question_factory import (
    QuestionFactory,
)
from src.application.factories.question_factory_builder import (
    QuestionFactoryBuilder,
)
from src.infrastructure.validators.question_record_validator import (
    QuestionRecordValidator,
)


class QuestionMapper:
    """
    Raw mapping -> Question entity mapper.
    """

    def __init__(
        self,
        *,
        factory: QuestionFactory | None = None,
    ) -> None:
        self._factory = (
            factory
            or QuestionFactoryBuilder.build_default()
        )

    def from_mapping(
        self,
        *,
        payload: Mapping[str, Any],
        index: int,
    ) -> Question:
        QuestionRecordValidator.validate(
            payload=payload,
            index=index,
        )

        return self._factory.create_from_payload(
            dict(payload),
        )