from __future__ import annotations

from typing import Protocol

from src.domain.enums.question_type import QuestionType


class QuestionTypeParser(Protocol):
    def parse(
        self,
        value: QuestionType | str,
    ) -> QuestionType:
        ...