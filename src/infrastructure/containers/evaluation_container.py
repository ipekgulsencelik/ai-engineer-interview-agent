from __future__ import annotations

from functools import cached_property

from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.infrastructure.containers.base_container import (
    BaseContainer,
)
from src.infrastructure.evaluators.mock_evaluator import (
    MockEvaluator,
)


class EvaluationContainer(BaseContainer):
    """
    Evaluation dependency container.
    """

    @cached_property
    def answer_evaluation_service(
        self,
    ) -> AnswerEvaluationService:
        return AnswerEvaluationService(
            evaluator=MockEvaluator(),
        )