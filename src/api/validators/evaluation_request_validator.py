from __future__ import annotations

from src.api.normalizers.difficulty_normalizer import (
    DifficultyNormalizer,
)
from src.api.normalizers.level_normalizer import (
    LevelNormalizer,
)
from src.api.normalizers.question_type_normalizer import (
    QuestionTypeNormalizer,
)


class EvaluationRequestValidator:
    """
    EvaluationRequest normalization facade.
    """

    @staticmethod
    def normalize_level(
        value: object,
    ) -> object:
        return LevelNormalizer.normalize(
            value,
        )

    @staticmethod
    def normalize_difficulty(
        value: object,
    ) -> object:
        return DifficultyNormalizer.normalize(
            value,
        )

    @staticmethod
    def normalize_question_type(
        value: object,
    ) -> object:
        return QuestionTypeNormalizer.normalize(
            value,
        )