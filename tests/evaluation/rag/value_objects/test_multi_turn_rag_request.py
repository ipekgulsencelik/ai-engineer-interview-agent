from __future__ import annotations

import pytest

from src.evaluation.rag.value_objects.multi_turn_rag_request import MultiTurnRAGRequest
from tests.evaluation.rag.factories import conversation_turn


def test_multi_turn_rag_request_should_expose_turn_count_and_has_turns() -> None:
    request = MultiTurnRAGRequest(conversation_id="c1", turns=(conversation_turn(),))
    assert request.turn_count == 1
    assert request.has_turns is True


def test_multi_turn_rag_request_should_reject_non_turn_items() -> None:
    with pytest.raises(ValueError):
        MultiTurnRAGRequest(conversation_id="c1", turns=(object(),))  # type: ignore[arg-type]
