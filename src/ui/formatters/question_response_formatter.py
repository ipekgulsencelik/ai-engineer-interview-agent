from __future__ import annotations

from src.ui.constants.question_metadata_labels import (
    CATEGORY_LABEL,
    DIFFICULTY_LABEL,
    LEVEL_LABEL,
    RETRIEVAL_SCORE_LABEL,
    TYPE_LABEL,
)
from src.ui.presentation.question_metadata_item import (
    QuestionMetadataItem,
)
from src.ui.schemas.question_response import (
    QuestionResponse,
)


class QuestionResponseFormatter:
    """
    UI presentation formatting utilities for QuestionResponse.
    """

    @staticmethod
    def format_score(
        *,
        score: float,
    ) -> str:
        return f"{score:.2f}"

    @staticmethod
    def format_difficulty(
        *,
        difficulty: int,
    ) -> str:
        return str(difficulty)

    @staticmethod
    def to_display_metadata(
        *,
        question: QuestionResponse,
    ) -> list[QuestionMetadataItem]:
        return [
            QuestionResponseFormatter._build_metadata_item(
                label=CATEGORY_LABEL,
                value=question.category,
            ),
            QuestionResponseFormatter._build_metadata_item(
                label=LEVEL_LABEL,
                value=question.level,
            ),
            QuestionResponseFormatter._build_metadata_item(
                label=TYPE_LABEL,
                value=question.question_type,
            ),
            QuestionResponseFormatter._build_metadata_item(
                label=DIFFICULTY_LABEL,
                value=QuestionResponseFormatter.format_difficulty(
                    difficulty=question.difficulty,
                ),
            ),
            QuestionResponseFormatter._build_metadata_item(
                label=RETRIEVAL_SCORE_LABEL,
                value=QuestionResponseFormatter.format_score(
                    score=question.final_score,
                ),
            ),
        ]

    @staticmethod
    def _build_metadata_item(
        *,
        label: str,
        value: str,
    ) -> QuestionMetadataItem:
        return QuestionMetadataItem(
            label=label,
            value=value,
        )