from __future__ import annotations

from src.evaluation.rag.counters.matched_token_counter import MatchedTokenCounter


def test_matched_token_counter_should_count_intersection_between_answer_and_chunk_tokens() -> None:
    assert MatchedTokenCounter.count(
        answer_tokens={"rag", "context", "answer"},
        chunk_tokens={"rag", "context", "retrieval"},
    ) == 2
