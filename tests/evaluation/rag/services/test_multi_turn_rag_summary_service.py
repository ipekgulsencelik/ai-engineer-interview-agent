from __future__ import annotations

from src.evaluation.rag.services.multi_turn_rag_summary_service import MultiTurnRAGSummaryService
from src.evaluation.rag.value_objects.multi_turn_rag_request import MultiTurnRAGRequest
from tests.evaluation.rag.factories import conversation_turn, turn_rag_result


def test_multi_turn_rag_summary_service_should_average_turn_results() -> None:
    result = MultiTurnRAGSummaryService().summarize(
        request=MultiTurnRAGRequest(conversation_id="conversation-1", turns=(conversation_turn(),)),
        turn_results=(
            turn_rag_result(turn_index=0, overall_score=1.0),
            turn_rag_result(turn_index=1, overall_score=0.5, faithfulness_score=0.5),
        ),
    )

    assert result.turn_count == 2
    assert result.average_faithfulness_score == 0.75
    assert result.overall_score == 0.75
