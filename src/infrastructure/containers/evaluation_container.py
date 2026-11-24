from __future__ import annotations

from collections.abc import Callable
from functools import cached_property

from src.application.parsers.evaluator_response_parser import (
    EvaluatorResponseParser,
)
from src.application.ports.llm_client import LLMClient
from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.application.validators.answer_validator import AnswerValidator
from src.domain.evaluation.evaluator import Evaluator
from src.infrastructure.containers.base_container import (
    BaseContainer,
)
from src.infrastructure.evaluators.fallback_evaluator import FallbackEvaluator
from src.infrastructure.evaluators.groq_rubric_evaluator import (
    GroqRubricEvaluator,
)
from src.infrastructure.evaluators.keyword_coverage_evaluator import (
    KeywordCoverageEvaluator,
)
from src.infrastructure.prompting.rubric_evaluation_prompt_builder import (
    RubricEvaluationPromptBuilder,
)


class EvaluationContainer(BaseContainer):
    """
    Evaluation dependency container.

    With an LLM client factory (GROQ_API_KEY configured) answers are graded by
    the Groq rubric evaluator, falling back to the offline keyword-coverage
    evaluator on provider errors. Without one, the offline evaluator is used.
    """

    def __init__(
        self,
        *,
        llm_client_factory: Callable[[], LLMClient] | None = None,
    ) -> None:
        self._llm_client_factory = llm_client_factory

    @property
    def uses_llm(self) -> bool:
        return self._llm_client_factory is not None

    @cached_property
    def evaluator(self) -> Evaluator:
        offline = KeywordCoverageEvaluator()
        if self._llm_client_factory is None:
            return offline
        return FallbackEvaluator(
            primary=GroqRubricEvaluator(
                llm_client=self._llm_client_factory(),
                prompt_builder=RubricEvaluationPromptBuilder(),
                response_parser=EvaluatorResponseParser(),
                answer_validator=AnswerValidator(),
            ),
            fallback=offline,
        )

    @cached_property
    def answer_evaluation_service(
        self,
    ) -> AnswerEvaluationService:
        return AnswerEvaluationService(
            evaluator=self.evaluator,
        )
