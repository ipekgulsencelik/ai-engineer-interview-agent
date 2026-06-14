from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.faithfulness_evaluation_request import FaithfulnessEvaluationRequest


def test_faithfulness_request_should_store_question_answer_and_context() -> None:
    request = FaithfulnessEvaluationRequest(question="q", generated_answer="a", retrieved_context="c")
    assert request.question == "q"
    assert request.generated_answer == "a"
    assert request.retrieved_context == "c"


def test_faithfulness_request_should_reject_empty_retrieved_context() -> None:
    with pytest.raises(ValueError):
        FaithfulnessEvaluationRequest(question="q", generated_answer="a", retrieved_context="")
