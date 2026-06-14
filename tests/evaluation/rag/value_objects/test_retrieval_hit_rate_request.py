from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.retrieval_hit_rate_request import RetrievalHitRateRequest


def test_retrieval_hit_rate_request_should_store_expected_chunk_and_top_k() -> None:
    request = RetrievalHitRateRequest(question="q", expected_chunk_id="c1", retrieved_chunk_ids=("c1",), top_k=1)
    assert request.expected_chunk_id == "c1"
    assert request.top_k == 1


def test_retrieval_hit_rate_request_should_reject_zero_top_k() -> None:
    with pytest.raises(ValueError):
        RetrievalHitRateRequest(question="q", expected_chunk_id="c1", retrieved_chunk_ids=(), top_k=0)
