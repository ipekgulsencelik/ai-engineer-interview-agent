from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.semantic_similarity_request import SemanticSimilarityRequest


def test_semantic_similarity_request_should_store_reference_and_candidate_text() -> None:
    request = SemanticSimilarityRequest(reference_text="reference", candidate_text="candidate")
    assert request.reference_text == "reference"
    assert request.candidate_text == "candidate"


def test_semantic_similarity_request_should_reject_empty_candidate_text() -> None:
    with pytest.raises(ValueError):
        SemanticSimilarityRequest(reference_text="reference", candidate_text="")
