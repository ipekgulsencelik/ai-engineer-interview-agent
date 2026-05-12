from __future__ import annotations

from src.application.parsers.evaluator_response_parser import (
    EvaluatorResponseParser,
)
from src.application.ports.evaluation_prompt_builder import (
    EvaluationPromptBuilder,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.application.validators.answer_validator import (
    AnswerValidator,
)
from src.domain.entities.question import Question
from src.domain.evaluation.evaluator import Evaluator
from src.domain.results.evaluation_result import EvaluationResult
from src.shared.logging.logger import logger


class GroqRubricEvaluator(Evaluator):
    """
    Groq tabanlı rubric-driven evaluator implementasyonudur.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_builder: EvaluationPromptBuilder,
        response_parser: EvaluatorResponseParser,
        answer_validator: AnswerValidator,
    ) -> None:
        self._llm_client = llm_client
        self._prompt_builder = prompt_builder
        self._response_parser = response_parser
        self._answer_validator = answer_validator

    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        self._answer_validator.validate(answer)

        logger.info(
            "Rubric evaluation started.",
            question_id=question.id,
            category=question.category,
            level=self._as_log_value(question.level),
            question_type=self._as_log_value(question.question_type),
        )

        try:
            prompt = self._prompt_builder.build(
                question=question,
                answer=answer,
            )

            llm_response = self._llm_client.generate(
                prompt=prompt,
            )

            result = self._response_parser.parse(
                llm_response,
            )

            logger.info(
                "Rubric evaluation completed.",
                question_id=question.id,
                score=result.score,
                confidence=result.metadata.confidence,
            )

            return result

        except Exception:
            logger.exception(
                "Rubric evaluation failed.",
                question_id=question.id,
            )
            raise

    @staticmethod
    def _as_log_value(value: object) -> object:
        return getattr(value, "value", value)