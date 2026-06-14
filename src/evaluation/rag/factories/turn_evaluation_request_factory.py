from __future__ import annotations

from src.evaluation.rag.value_objects.answer_relevancy_request import (
    AnswerRelevancyRequest,
)
from src.evaluation.rag.value_objects.context_precision_request import (
    ContextPrecisionRequest,
)
from src.evaluation.rag.value_objects.faithfulness_evaluation_request import (
    FaithfulnessEvaluationRequest,
)
from src.evaluation.rag.value_objects.conversation_turn import (
    ConversationTurn,
)


class TurnEvaluationRequestFactory:
    """
    Builds single-turn RAG metric requests
    from conversation turns.
    """

    @staticmethod
    def build_faithfulness_request(
        *,
        turn: ConversationTurn,
    ) -> FaithfulnessEvaluationRequest | None:
        if turn.retrieved_context is None:
            return None

        return FaithfulnessEvaluationRequest(
            question=turn.user_message,
            generated_answer=turn.assistant_message,
            retrieved_context=turn.retrieved_context,
            model_name=turn.model_name,
            evaluator_name=None,
        )

    @staticmethod
    def build_answer_relevancy_request(
        *,
        turn: ConversationTurn,
    ) -> AnswerRelevancyRequest:
        return AnswerRelevancyRequest(
            question=turn.user_message,
            generated_answer=turn.assistant_message,
            model_name=turn.model_name,
            evaluator_name=None,
        )

    @staticmethod
    def build_context_precision_request(
        *,
        turn: ConversationTurn,
    ) -> ContextPrecisionRequest | None:
        if turn.retrieved_context is None:
            return None

        return ContextPrecisionRequest(
            question=turn.user_message,
            generated_answer=turn.assistant_message,
            retrieved_context=turn.retrieved_context,
            model_name=turn.model_name,
            evaluator_name=None,
        )