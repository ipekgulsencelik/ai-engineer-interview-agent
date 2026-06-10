from __future__ import annotations

from src.domain.entities.question import Question
from src.infrastructure.errors.question_collection_error import (
    QuestionCollectionError,
)


class QuestionCollectionValidator:
    """
    Question collection validation helper.
    """

    @staticmethod
    def validate_unique_ids(
        questions: list[Question],
    ) -> None:
        seen_ids: set[str] = set()

        for question in questions:
            if question.id in seen_ids:
                raise QuestionCollectionError(
                    f"Duplicate question id detected: "
                    f"{question.id}"
                )

            seen_ids.add(question.id)