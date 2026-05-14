from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.infrastructure.validations.question_chroma.chroma_question_metadata_validator import (
    ChromaQuestionMetadataValidator,
)
from src.infrastructure.vector_stores.question_chroma.chroma_question_types import (
    ChromaQueryResults,
    QuestionMetadata,
)


class ChromaQuestionResultMapper:
    """Maps raw Chroma query payloads into domain `Question` entities."""

    @staticmethod
    def to_questions(results: ChromaQueryResults) -> list[Question]:
        metadata_batches = results.get("metadatas") or []
        if not metadata_batches:
            return []

        return [
            ChromaQuestionResultMapper._to_question(metadata)
            for metadata in metadata_batches[0]
        ]

    @staticmethod
    def _to_question(metadata: QuestionMetadata) -> Question:
        ChromaQuestionMetadataValidator.validate(metadata)
        return Question(
            id=str(metadata["id"]),
            text=str(metadata["text"]),
            category=QuestionCategory(metadata["category"]),
            level=Level(metadata["level"]),
            difficulty=Difficulty(metadata["difficulty"]),
            question_type=QuestionType(metadata["question_type"]),
            expected_points=metadata.get("expected_points", []),
            keywords=metadata.get("keywords", []),
            market_weight=float(metadata.get("market_weight", 1.0)),
        )