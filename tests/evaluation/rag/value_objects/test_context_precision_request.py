from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.context_precision_request import ContextPrecisionRequest


def test_context_precision_request_should_store_expected_answer_when_present() -> None:
    request = ContextPrecisionRequest(question="q", generated_answer="a", retrieved_context="c", expected_answer="e")
    assert request.expected_answer == "e"


def test_context_precision_request_should_reject_empty_generated_answer() -> None:
    with pytest.raises(ValueError):
        ContextPrecisionRequest(question="q", generated_answer="", retrieved_context="c")
