from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.context_recall_request import ContextRecallRequest


def test_context_recall_request_should_store_expected_and_retrieved_context() -> None:
    request = ContextRecallRequest(question="q", expected_answer="a", expected_context="ec", retrieved_context="rc")
    assert request.expected_context == "ec"
    assert request.retrieved_context == "rc"


def test_context_recall_request_should_reject_empty_expected_context() -> None:
    with pytest.raises(ValueError):
        ContextRecallRequest(question="q", expected_answer="a", expected_context="", retrieved_context="rc")
