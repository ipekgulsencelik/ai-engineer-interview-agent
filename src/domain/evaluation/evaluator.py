from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.domain.entities.question import Question
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class Evaluator(ABC):
    """
    Candidate answer evaluation contract.
    """

    @abstractmethod
    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        ...