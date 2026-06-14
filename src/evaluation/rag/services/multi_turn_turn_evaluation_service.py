from __future__ import annotations

from src.evaluation.rag.calculators.turn_rag_score_calculator import (
    TurnRAGScoreCalculator,
)
from src.evaluation.rag.evaluators.answer_relevancy_evaluator import (
    AnswerRelevancyEvaluator,
)
from src.evaluation.rag.evaluators.context_precision_evaluator import (
    ContextPrecisionEvaluator,
)
from src.evaluation.rag.evaluators.faithfulness_evaluator import (
    FaithfulnessEvaluator,
)
from src.evaluation.rag.factories.turn_evaluation_request_factory import (
    TurnEvaluationRequestFactory,
)
from src.evaluation.rag.factories.turn_rag_result_factory import (
    TurnRAGResultFactory,
)
from src.evaluation.rag.value_objects.conversation_turn import (
    ConversationTurn,
)
from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


class MultiTurnTurnEvaluationService:
    """
    Evaluates individual turns in a multi-turn RAG conversation.
    """

    def __init__(
        self,
        *,
        faithfulness_evaluator: FaithfulnessEvaluator | None = None,
        answer_relevancy_evaluator: AnswerRelevancyEvaluator | None = None,
        context_precision_evaluator: ContextPrecisionEvaluator | None = None,
        request_factory: TurnEvaluationRequestFactory | None = None,
        turn_score_calculator: TurnRAGScoreCalculator | None = None,
        turn_result_factory: TurnRAGResultFactory | None = None,
    ) -> None:
        self._faithfulness_evaluator = (
            faithfulness_evaluator or FaithfulnessEvaluator()
        )
        self._answer_relevancy_evaluator = (
            answer_relevancy_evaluator or AnswerRelevancyEvaluator()
        )
        self._context_precision_evaluator = (
            context_precision_evaluator or ContextPrecisionEvaluator()
        )
        self._request_factory = (
            request_factory or TurnEvaluationRequestFactory()
        )
        self._turn_score_calculator = (
            turn_score_calculator or TurnRAGScoreCalculator()
        )
        self._turn_result_factory = (
            turn_result_factory or TurnRAGResultFactory()
        )

    def evaluate_turns(
        self,
        *,
        turns: tuple[ConversationTurn, ...],
    ) -> tuple[TurnRAGResult, ...]:
        return tuple(
            self.evaluate_turn(
                turn=turn,
            )
            for turn in turns
        )

    def evaluate_turn(
        self,
        *,
        turn: ConversationTurn,
    ) -> TurnRAGResult:
        faithfulness_score = self._evaluate_faithfulness(
            turn=turn,
        )

        answer_relevancy_score = self._evaluate_answer_relevancy(
            turn=turn,
        )

        context_precision_score = self._evaluate_context_precision(
            turn=turn,
        )

        overall_score = self._turn_score_calculator.calculate(
            faithfulness_score=faithfulness_score,
            answer_relevancy_score=answer_relevancy_score,
            context_precision_score=context_precision_score,
        )

        return self._turn_result_factory.create(
            turn_index=turn.turn_index,
            faithfulness_score=faithfulness_score,
            answer_relevancy_score=answer_relevancy_score,
            context_precision_score=context_precision_score,
            overall_score=overall_score,
        )

    def _evaluate_faithfulness(
        self,
        *,
        turn: ConversationTurn,
    ) -> float:
        request = self._request_factory.build_faithfulness_request(
            turn=turn,
        )

        if request is None:
            return 0.0

        return self._faithfulness_evaluator.evaluate(
            request=request,
        )

    def _evaluate_answer_relevancy(
        self,
        *,
        turn: ConversationTurn,
    ) -> float:
        request = self._request_factory.build_answer_relevancy_request(
            turn=turn,
        )

        return self._answer_relevancy_evaluator.evaluate(
            request=request,
        )

    def _evaluate_context_precision(
        self,
        *,
        turn: ConversationTurn,
    ) -> float:
        request = self._request_factory.build_context_precision_request(
            turn=turn,
        )

        if request is None:
            return 0.0

        return self._context_precision_evaluator.evaluate(
            request=request,
        )