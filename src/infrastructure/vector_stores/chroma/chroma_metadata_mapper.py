from __future__ import annotations

from typing import Any

from src.domain.entities.question import Question


class ChromaMetadataMapper:
    """Maps Question entities to Chroma-safe metadata payloads."""

    @classmethod
    def from_question(cls, question: Question) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "question_id": question.id,
            "category": cls._to_value(question.category),
            "level": cls._to_value(question.level),
            "difficulty": question.difficulty,
            "question_type": cls._to_value(question.question_type),
            "market_weight": question.market_weight,
            "followup_allowed": question.followup_allowed,
        }
        return cls._remove_none_values(metadata)

    @staticmethod
    def _to_value(value: object) -> object:
        if hasattr(value, "value"):
            return value.value
        return value

    @staticmethod
    def _remove_none_values(metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in metadata.items()
            if value is not None
        }