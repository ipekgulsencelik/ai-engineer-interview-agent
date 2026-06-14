from __future__ import annotations

import pytest

from tests.evaluation.rag.factories import conversation_turn


def test_conversation_turn_should_expose_retrieval_model_and_retriever_flags() -> None:
    turn = conversation_turn()
    assert turn.has_retrieved_context is True
    assert turn.has_model is True
    assert turn.has_retriever is True


def test_conversation_turn_should_reject_negative_turn_index() -> None:
    with pytest.raises(ValueError):
        conversation_turn(turn_index=-1)
