from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.application.models.llm_request import LLMRequest
from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.metadata.evaluation_metadata import EvaluationMetadata
from src.domain.results.evaluation_result import EvaluationResult
from src.infrastructure.evaluators.groq_rubric_evaluator import (
    GroqRubricEvaluator,
)


@dataclass
class FakeAnswerValidator:
    called_with: str | None = None
    should_raise: bool = False

    def validate(
        self,
        answer: str,
    ) -> None:
        self.called_with = answer

        if self.should_raise:
            raise ValueError(
                "invalid answer"
            )


@dataclass
class FakePromptBuilder:
    called_question: Question | None = None
    called_answer: str | None = None
    prompt: str = "generated prompt"

    def build(
        self,
        *,
        question: Question,
        answer: str,
    ) -> str:
        self.called_question = question
        self.called_answer = answer

        return self.prompt


@dataclass
class FakeLLMClient:
    called_request: LLMRequest | None = None
    response: LLMResponse | None = None
    should_raise: bool = False

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        self.called_request = request

        if self.should_raise:
            raise RuntimeError(
                "llm failed"
            )

        if self.response is None:
            raise RuntimeError(
                "fake response was not configured"
            )

        return self.response


@dataclass
class FakeResponseParser:
    called_response: LLMResponse | None = None
    result: EvaluationResult | None = None
    should_raise: bool = False

    def parse(
        self,
        response: LLMResponse,
    ) -> EvaluationResult:
        self.called_response = response

        if self.should_raise:
            raise ValueError(
                "parse failed"
            )

        if self.result is None:
            raise RuntimeError(
                "fake result was not configured"
            )

        return self.result


def build_question() -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category=QuestionCategory.RAG,
        level=Level.JR,
        difficulty=1,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=[
            "Retrieval",
            "Generation",
        ],
        keywords=[
            "embedding",
            "vector database",
        ],
    )


def build_llm_response() -> LLMResponse:
    return LLMResponse(
        text='{"score": 8}',
        metadata=LLMResponseMetadata(
            model="llama3-70b-8192",
            prompt_tokens=10,
            completion_tokens=32,
            total_tokens=42,
            latency_seconds=0.12,
            finish_reason="stop",
            raw_response=None,
        ),
    )


def build_evaluation_result() -> EvaluationResult:
    return EvaluationResult(
        score=8.0,
        feedback="Good answer.",
        technical_accuracy=8.0,
        depth=7.0,
        communication=9.0,
        metadata=EvaluationMetadata(
            confidence=0.9,
            rubric_version="v1",
            missing_keywords=[
                "chunking",
            ],
            follow_up_question="How would you improve retrieval quality?",
        ),
    )


def test_evaluate_orchestrates_dependencies_in_order() -> None:
    question = build_question()
    answer = "RAG combines retrieval with generation."

    llm_response = build_llm_response()
    evaluation_result = build_evaluation_result()

    answer_validator = FakeAnswerValidator()

    prompt_builder = FakePromptBuilder(
        prompt="generated prompt",
    )

    llm_client = FakeLLMClient(
        response=llm_response,
    )

    response_parser = FakeResponseParser(
        result=evaluation_result,
    )

    evaluator = GroqRubricEvaluator(
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        response_parser=response_parser,
        answer_validator=answer_validator,
    )

    result = evaluator.evaluate(
        question=question,
        answer=answer,
    )

    assert result == evaluation_result

    assert answer_validator.called_with == answer

    assert prompt_builder.called_question == question
    assert prompt_builder.called_answer == answer

    assert llm_client.called_request == LLMRequest(
        prompt="generated prompt",
    )

    assert response_parser.called_response == llm_response


def test_evaluate_stops_when_answer_validation_fails() -> None:
    question = build_question()
    answer = ""

    answer_validator = FakeAnswerValidator(
        should_raise=True,
    )

    prompt_builder = FakePromptBuilder()

    llm_client = FakeLLMClient(
        response=build_llm_response(),
    )

    response_parser = FakeResponseParser(
        result=build_evaluation_result(),
    )

    evaluator = GroqRubricEvaluator(
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        response_parser=response_parser,
        answer_validator=answer_validator,
    )

    with pytest.raises(
        ValueError,
        match="invalid answer",
    ):
        evaluator.evaluate(
            question=question,
            answer=answer,
        )

    assert answer_validator.called_with == answer
    assert prompt_builder.called_question is None
    assert llm_client.called_request is None
    assert response_parser.called_response is None


def test_evaluate_propagates_llm_errors() -> None:
    question = build_question()
    answer = "Candidate answer."

    answer_validator = FakeAnswerValidator()

    prompt_builder = FakePromptBuilder(
        prompt="generated prompt",
    )

    llm_client = FakeLLMClient(
        should_raise=True,
    )

    response_parser = FakeResponseParser(
        result=build_evaluation_result(),
    )

    evaluator = GroqRubricEvaluator(
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        response_parser=response_parser,
        answer_validator=answer_validator,
    )

    with pytest.raises(
        RuntimeError,
        match="llm failed",
    ):
        evaluator.evaluate(
            question=question,
            answer=answer,
        )

    assert answer_validator.called_with == answer
    assert prompt_builder.called_question == question
    assert prompt_builder.called_answer == answer
    assert llm_client.called_request == LLMRequest(
        prompt="generated prompt",
    )
    assert response_parser.called_response is None


def test_evaluate_propagates_parser_errors() -> None:
    question = build_question()
    answer = "Candidate answer."

    llm_response = build_llm_response()

    answer_validator = FakeAnswerValidator()

    prompt_builder = FakePromptBuilder(
        prompt="generated prompt",
    )

    llm_client = FakeLLMClient(
        response=llm_response,
    )

    response_parser = FakeResponseParser(
        should_raise=True,
    )

    evaluator = GroqRubricEvaluator(
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        response_parser=response_parser,
        answer_validator=answer_validator,
    )

    with pytest.raises(
        ValueError,
        match="parse failed",
    ):
        evaluator.evaluate(
            question=question,
            answer=answer,
        )

    assert answer_validator.called_with == answer
    assert prompt_builder.called_question == question
    assert prompt_builder.called_answer == answer
    assert llm_client.called_request == LLMRequest(
        prompt="generated prompt",
    )
    assert response_parser.called_response == llm_response