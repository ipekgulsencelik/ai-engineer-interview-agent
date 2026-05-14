from __future__ import annotations

import math

from src.domain.entities.question import Question
from src.domain.enums.level import Level


class ChromaQuestionVectorStoreValidator:
    """Validation rules for ChromaQuestionVectorStore boundary inputs."""

    @staticmethod
    def validate_init(*, persist_directory: str, collection_name: str) -> None:
        if not isinstance(persist_directory, str) or not persist_directory.strip():
            raise ValueError("persist_directory must be a non-empty string")

        if not isinstance(collection_name, str) or not collection_name.strip():
            raise ValueError("collection_name must be a non-empty string")

    @staticmethod
    def validate_search(*, embedding: list[float], top_k: int, level: Level) -> None:
        if not isinstance(embedding, list) or not embedding:
            raise ValueError("embedding must be a non-empty list[float]")

        if not all(isinstance(value, (int, float)) for value in embedding):
            raise ValueError("embedding must contain only numeric values")

        if not all(math.isfinite(float(value)) for value in embedding):
            raise ValueError("embedding must contain only finite numeric values")

        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if not isinstance(level, Level):
            raise TypeError("level must be an instance of Level")


    @staticmethod
    def validate_add_question(*, question: Question, embedding: list[float]) -> None:
        if not isinstance(question, Question):
            raise TypeError("question must be an instance of Question")

        if not isinstance(embedding, list) or not embedding:
            raise ValueError("embedding must be a non-empty list[float]")

        if not all(isinstance(value, (int, float)) for value in embedding):
            raise ValueError("embedding must contain only numeric values")

        if not all(math.isfinite(float(value)) for value in embedding):
            raise ValueError("embedding must contain only finite numeric values")
