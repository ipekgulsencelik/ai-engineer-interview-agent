from __future__ import annotations

from src.domain.entities.question import Question


class QuestionCollectionValidator:
    """Collection-level validation for loaded Question entities."""

    @staticmethod
    def validate_unique_ids(questions: list[Question]) -> None:
        seen_ids: set[str] = set()
        duplicate_ids: set[str] = set()

        for question in questions:
            if question.id in seen_ids:
                duplicate_ids.add(question.id)
            seen_ids.add(question.id)

        if duplicate_ids:
            raise ValueError(
                f"Duplicate question ids found: {sorted(duplicate_ids)}"
            )