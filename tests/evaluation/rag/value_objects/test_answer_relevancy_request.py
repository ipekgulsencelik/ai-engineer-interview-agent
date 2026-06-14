from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.answer_relevancy_request import AnswerRelevancyRequest


def test_answer_relevancy_request_should_store_required_and_optional_fields() -> None:
    request = AnswerRelevancyRequest(question="q", generated_answer="a", model_name="m")
    assert request.question == "q"
    assert request.generated_answer == "a"
    assert request.model_name == "m"


def test_answer_relevancy_request_should_reject_empty_question() -> None:
    with pytest.raises(ValueError):
        AnswerRelevancyRequest(question="", generated_answer="a")
