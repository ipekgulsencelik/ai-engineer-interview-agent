from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import LexicalOverlapCalculator


def test_lexical_overlap_should_return_supported_token_ratio() -> None:
    assert LexicalOverlapCalculator.calculate(
        answer_tokens={"rag", "grounded"},
        context_tokens={"rag"},
    ) == 0.5


def test_lexical_overlap_should_return_zero_when_answer_tokens_are_empty() -> None:
    assert LexicalOverlapCalculator.calculate(
        answer_tokens=set(),
        context_tokens={"rag"},
    ) == 0.0


def test_lexical_overlap_should_return_zero_when_context_tokens_are_empty() -> None:
    assert LexicalOverlapCalculator.calculate(
        answer_tokens={"rag"},
        context_tokens=set(),
    ) == 0.0
