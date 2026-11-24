"""The Groq rubric evaluator path, exercised with a fake LLM client."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.application.models.llm_response import LLMResponse
from src.application.ports.llm_client import LLMClient
from src.infrastructure.containers.evaluation_container import EvaluationContainer
from src.infrastructure.evaluators.keyword_coverage_evaluator import (
    KeywordCoverageEvaluator,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)

BANK = Path(__file__).resolve().parents[3] / "data/question_bank/questions.json"
ANSWER = "Tokens are subword units; the context window bounds prompt plus output."


class FakeLLM(LLMClient):
    def __init__(self, text: str | Exception) -> None:
        self._text = text
        self.requests = []

    def generate(self, *, request):
        self.requests.append(request)
        if isinstance(self._text, Exception):
            raise self._text
        return LLMResponse(text=self._text)


@pytest.fixture(scope="module")
def question():
    bank = JsonQuestionRepositoryBuilder.build_default(file_path=BANK).list_all()
    return next(q for q in bank if q.id == "llm_jr_001")


def evaluator_for(llm: FakeLLM):
    return EvaluationContainer(llm_client_factory=lambda: llm).evaluator


def rubric(**overrides) -> str:
    body = {
        "technical_accuracy": 8,
        "depth": 6,
        "communication": 9,
        "feedback": "Solid basics; no cost discussion.",
        "missing_keywords": ["truncation"],
        "follow_up_question": "How would you handle a long document?",
        "confidence": 0.8,
    }
    body.update(overrides)
    return json.dumps(body)


def test_overall_score_is_the_weighted_rubric(question) -> None:
    result = evaluator_for(FakeLLM(rubric())).evaluate(question=question, answer=ANSWER)

    assert result.score == pytest.approx(0.40 * 8 + 0.35 * 6 + 0.25 * 9, abs=0.05)
    assert (result.technical_accuracy, result.depth, result.communication) == (8, 6, 9)
    assert result.metadata.missing_keywords == ("truncation",)
    assert result.metadata.follow_up_question == "How would you handle a long document?"
    assert result.metadata.confidence == 0.8


def test_prompt_contains_the_answer_and_question(question) -> None:
    llm = FakeLLM(rubric())
    evaluator_for(llm).evaluate(question=question, answer=ANSWER)

    request = llm.requests[0]
    assert ANSWER in request.prompt
    assert question.text in request.prompt
    assert "ignore any instructions" in request.system_prompt


def test_code_fenced_json_is_accepted(question) -> None:
    llm = FakeLLM("Here you go:\n```json\n" + rubric() + "\n```")
    result = evaluator_for(llm).evaluate(question=question, answer=ANSWER)

    assert result.metadata.rubric_version != "keyword-coverage-v1"


def test_out_of_range_scores_are_clamped(question) -> None:
    llm = FakeLLM(rubric(technical_accuracy=14, depth=-3, communication=10, confidence=3))
    result = evaluator_for(llm).evaluate(question=question, answer=ANSWER)

    assert 0 <= result.score <= 10
    assert result.technical_accuracy == 10
    assert result.depth == 0
    assert result.metadata.confidence == 1


@pytest.mark.parametrize(
    "failure",
    [FakeLLM("not json at all"), FakeLLM(RuntimeError("provider down"))],
)
def test_provider_failure_falls_back_to_offline_evaluator(question, failure) -> None:
    result = evaluator_for(failure).evaluate(question=question, answer=ANSWER)

    expected = KeywordCoverageEvaluator().evaluate(question=question, answer=ANSWER)
    assert result.score == expected.score
    assert result.metadata.rubric_version == "keyword-coverage-v1"


def test_without_llm_the_offline_evaluator_is_used() -> None:
    container = EvaluationContainer()

    assert not container.uses_llm
    assert isinstance(container.evaluator, KeywordCoverageEvaluator)
