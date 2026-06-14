from __future__ import annotations

from src.evaluation.rag.interpreters.multi_turn_rag_interpreter import MultiTurnRAGInterpreter


def test_multi_turn_rag_interpreter_should_return_passed_for_high_score() -> None:
    assert MultiTurnRAGInterpreter().interpret(overall_score=0.95) == "multi_turn_rag_passed"


def test_multi_turn_rag_interpreter_should_return_failed_for_low_score() -> None:
    assert MultiTurnRAGInterpreter().interpret(overall_score=0.1) == "multi_turn_rag_failed"
