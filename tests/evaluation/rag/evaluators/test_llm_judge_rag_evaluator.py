from __future__ import annotations

from src.evaluation.rag.evaluators.llm_judge_rag_evaluator import LLMJudgeRAGEvaluator
from src.evaluation.rag.value_objects.llm_judge_request import LLMJudgeRequest


def test_llm_judge_rag_evaluator_should_build_prompt_and_parse_response() -> None:
    evaluator = LLMJudgeRAGEvaluator()
    request = LLMJudgeRequest(question="q", generated_answer="a", retrieved_context="c", evaluation_criteria="criteria")

    prompt = evaluator.build_prompt(request=request)
    result = evaluator.parse_response(response='{"score": 0.8, "reason": "ok"}')

    assert "criteria" in prompt
    assert result.score == 0.8
    assert result.reason == "ok"

from src.evaluation.rag.value_objects.llm_judge_result import LLMJudgeResult


class _PromptBuilderSpy:
    def __init__(self) -> None:
        self.called_with: LLMJudgeRequest | None = None

    def build(self, *, request: LLMJudgeRequest) -> str:
        self.called_with = request
        return "custom prompt"


class _ResponseParserSpy:
    def __init__(self) -> None:
        self.called_with: str | None = None

    def parse(self, *, response: str) -> LLMJudgeResult:
        self.called_with = response
        return LLMJudgeResult(score=0.4, reason="custom")


def test_llm_judge_rag_evaluator_should_depend_on_prompt_and_parser_protocols() -> None:
    prompt_builder = _PromptBuilderSpy()
    response_parser = _ResponseParserSpy()
    evaluator = LLMJudgeRAGEvaluator(
        prompt_builder=prompt_builder,
        response_parser=response_parser,
    )
    request = LLMJudgeRequest(
        question="q",
        generated_answer="a",
        retrieved_context="c",
        evaluation_criteria="criteria",
    )

    assert evaluator.build_prompt(request=request) == "custom prompt"
    assert prompt_builder.called_with == request

    result = evaluator.parse_response(response="raw response")
    assert response_parser.called_with == "raw response"
    assert result == LLMJudgeResult(score=0.4, reason="custom")
