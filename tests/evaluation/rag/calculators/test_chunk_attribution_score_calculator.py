from __future__ import annotations

from src.evaluation.rag.calculators.chunk_attribution_score_calculator import ChunkAttributionScoreCalculator


def test_chunk_attribution_score_should_divide_matched_tokens_by_answer_token_count() -> None:
    assert ChunkAttributionScoreCalculator.calculate(
        matched_tokens=2,
        answer_token_count=4,
    ) == 0.5


def test_chunk_attribution_score_should_return_zero_without_answer_tokens() -> None:
    assert ChunkAttributionScoreCalculator.calculate(
        matched_tokens=2,
        answer_token_count=0,
    ) == 0.0
