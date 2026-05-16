from __future__ import annotations

from typing import Protocol

from src.domain.enums.question_category import QuestionCategory


class QuestionCategoryParser(Protocol):
    def parse(
        self,
        value: QuestionCategory | str,
    ) -> QuestionCategory:
        ...