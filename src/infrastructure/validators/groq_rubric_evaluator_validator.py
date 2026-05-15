from __future__ import annotations

from src.application.parsers.evaluator_response_parser import (
    EvaluatorResponseParser,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.domain.entities.question import Question
from src.infrastructure.prompting.rubric_prompt_builder import (
    RubricPromptBuilder,
)
from src.application.validators.answer_validator import (
    AnswerValidator,
)


class GroqRubricEvaluatorValidator:
    """
    GroqRubricEvaluator validation rules.
    """

    @staticmethod
    def validate_dependencies(
        *,
        llm_client: LLMClient,
        prompt_builder: RubricPromptBuilder,
        response_parser: EvaluatorResponseParser,
        answer_validator: AnswerValidator,
    ) -> None:
        if not isinstance(
            llm_client,
            LLMClient,
        ):
            raise TypeError(
                "llm_client must be LLMClient."
            )

        if not isinstance(
            prompt_builder,
            RubricPromptBuilder,
        ):
            raise TypeError(
                "prompt_builder must be "
                "RubricPromptBuilder."
            )

        if not isinstance(
            response_parser,
            EvaluatorResponseParser,
        ):
            raise TypeError(
                "response_parser must be "
                "EvaluatorResponseParser."
            )

        if not isinstance(
            answer_validator,
            AnswerValidator,
        ):
            raise TypeError(
                "answer_validator must be "
                "AnswerValidator."
            )

    @staticmethod
    def validate_input(
        *,
        question: Question,
        answer: str,
    ) -> None:
        if not isinstance(question, Question,):
            raise TypeError("question must be Question.")

        if not isinstance(answer, str,):
            raise TypeError("answer must be string.")

        if not answer.strip():
            raise ValueError("answer cannot be empty.")