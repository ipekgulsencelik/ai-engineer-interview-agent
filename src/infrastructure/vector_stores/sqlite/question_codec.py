"""Lossless conversion between Question entities and persisted JSON records."""

from __future__ import annotations

import json
from dataclasses import asdict

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.infrastructure.errors.vector_store_error import VectorStoreError


class QuestionCodec:
    """Keep domain serialization out of the SQLite persistence adapter."""

    @staticmethod
    def encode(question: Question) -> str:
        return json.dumps(asdict(question), ensure_ascii=False, sort_keys=True)

    @staticmethod
    def decode(raw: str) -> Question:
        try:
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("question payload must be an object")
            payload["category"] = QuestionCategory(payload["category"])
            payload["level"] = Level(payload["level"])
            payload["question_type"] = QuestionType(payload["question_type"])
            return Question(**payload)
        except (KeyError, TypeError, ValueError) as exc:
            raise VectorStoreError("Invalid persisted question record.") from exc
