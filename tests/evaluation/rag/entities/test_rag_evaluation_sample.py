from __future__ import annotations

import pytest

from tests.evaluation.rag.factories import rag_sample


def test_rag_evaluation_sample_should_expose_expected_answer_context_and_chunk_flags() -> None:
    sample = rag_sample()

    assert sample.has_expected_answer is True
    assert sample.has_expected_context is True
    assert sample.has_expected_chunks is True


def test_rag_evaluation_sample_should_reject_empty_required_fields() -> None:
    with pytest.raises(ValueError):
        rag_sample(sample_id="")
