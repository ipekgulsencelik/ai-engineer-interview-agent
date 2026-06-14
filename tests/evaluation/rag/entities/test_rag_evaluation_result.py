from __future__ import annotations

import pytest

from tests.evaluation.rag.factories import rag_result


def test_rag_evaluation_result_should_expose_failure_hallucination_and_context_hit_rate() -> None:
    result = rag_result(
        passed=False,
        hallucination_detected=True,
        relevant_context_count=1,
        retrieved_context_count=4,
    )

    assert result.failed is True
    assert result.has_hallucination is True
    assert result.has_expected_answer is True
    assert result.context_hit_rate == 0.25


def test_rag_evaluation_result_context_hit_rate_should_be_zero_without_retrieved_contexts() -> None:
    assert rag_result(
        retrieved_context_count=0,
        relevant_context_count=0,
    ).context_hit_rate == 0.0


def test_rag_evaluation_result_should_reject_scores_outside_ratio_bounds() -> None:
    with pytest.raises(ValueError):
        rag_result(overall_score=1.5)
