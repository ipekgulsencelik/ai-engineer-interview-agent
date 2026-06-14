from __future__ import annotations

from src.evaluation.rag.parsers.llm_judge_response_parser import LLMJudgeResponseParser


def test_llm_judge_response_parser_should_parse_json_score_and_reason() -> None:
    result = LLMJudgeResponseParser.parse(response='{"score": 0.75, "reason": "grounded"}')

    assert result.score == 0.75
    assert result.reason == "grounded"
