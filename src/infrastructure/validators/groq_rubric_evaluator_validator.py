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
from src.domain.validators.base_schema_validator import (
    BaseSchemaValidator,
)


class GroqRubricEvaluatorValidator(
    BaseSchemaValidator,
):
    """
    GroqRubricEvaluator validation helper.
    """

    @classmethod
    def validate_dependencies(
        cls,
        *,
        llm_client: LLMClient,
        prompt_builder: EvaluationPromptBuilder,
        response_parser: EvaluatorResponseParser,
        answer_validator: AnswerValidator,
    ) -> None:
        cls._validate_has_callable(
            value=llm_client,
            method_name="generate",
            field_name="llm_client",
        )

        cls._validate_has_callable(
            value=prompt_builder,
            method_name="build",
            field_name="prompt_builder",
        )

        cls.validate_model_type(
            value=response_parser,
            expected_type=EvaluatorResponseParser,
            field_name="response_parser",
        )

        cls.validate_model_type(
            value=answer_validator,
            expected_type=AnswerValidator,
            field_name="answer_validator",
        )

    @classmethod
    def validate_input(
        cls,
        *,
        question: Question,
        answer: str,
    ) -> None:
        cls.validate_model_type(
            value=question,
            expected_type=Question,
            field_name="question",
        )

        cls._validate_required_string(
            field_name="answer",
            value=answer,
        )

    @staticmethod
    def _validate_required_string(
        *,
        field_name: str,
        value: str,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_has_callable(
        *,
        value: object,
        method_name: str,
        field_name: str,
    ) -> None:
        method = getattr(
            value,
            method_name,
            None,
        )

        if not callable(method):
            raise TypeError(
                f"{field_name} must implement callable "
                f"{method_name}()."
            )