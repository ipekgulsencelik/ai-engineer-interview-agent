from __future__ import annotations

from src.evaluation.rag.calculators.conversation_rag_score_calculator import (
    ConversationRAGScoreCalculator,
)
from src.evaluation.rag.calculators.rag_average_metric_calculator import (
    RAGAverageMetricCalculator,
)
from src.evaluation.rag.factories.multi_turn_rag_result_factory import (
    MultiTurnRAGResultFactory,
)
from src.evaluation.rag.interpreters.multi_turn_rag_interpreter import (
    MultiTurnRAGInterpreter,
)
from src.evaluation.rag.requests.multi_turn_rag_request import (
    MultiTurnRAGRequest,
)
from src.evaluation.rag.value_objects.multi_turn_rag_result import (
    MultiTurnRAGResult,
)
from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


class MultiTurnRAGSummaryService:
    """
    Builds final multi-turn RAG evaluation result from turn results.
    """

    def __init__(
        self,
        *,
        conversation_score_calculator: (
            ConversationRAGScoreCalculator | None
        ) = None,
        average_calculator: RAGAverageMetricCalculator | None = None,
        result_factory: MultiTurnRAGResultFactory | None = None,
        interpreter: MultiTurnRAGInterpreter | None = None,
    ) -> None:
        self._conversation_score_calculator = (
            conversation_score_calculator
            or ConversationRAGScoreCalculator()
        )
        self._average_calculator = (
            average_calculator or RAGAverageMetricCalculator()
        )
        self._result_factory = (
            result_factory or MultiTurnRAGResultFactory()
        )
        self._interpreter = (
            interpreter or MultiTurnRAGInterpreter()
        )

    def summarize(
        self,
        *,
        request: MultiTurnRAGRequest,
        turn_results: tuple[TurnRAGResult, ...],
    ) -> MultiTurnRAGResult:
        overall_score = self._calculate_conversation_score(
            turn_results=turn_results,
        )

        return self._result_factory.create(
            conversation_id=request.conversation_id,
            turn_results=turn_results,
            average_faithfulness_score=(
                self._calculate_average_faithfulness_score(
                    turn_results=turn_results,
                )
            ),
            average_answer_relevancy_score=(
                self._calculate_average_answer_relevancy_score(
                    turn_results=turn_results,
                )
            ),
            average_context_precision_score=(
                self._calculate_average_context_precision_score(
                    turn_results=turn_results,
                )
            ),
            overall_score=overall_score,
            interpretation=self._interpreter.interpret(
                overall_score=overall_score,
            ),
            notes=request.notes,
        )

    def _calculate_conversation_score(
        self,
        *,
        turn_results: tuple[TurnRAGResult, ...],
    ) -> float:
        return self._conversation_score_calculator.calculate(
            turn_scores=tuple(
                result.overall_score
                for result in turn_results
            ),
        )

    def _calculate_average_faithfulness_score(
        self,
        *,
        turn_results: tuple[TurnRAGResult, ...],
    ) -> float:
        return self._average_calculator.calculate(
            values=tuple(
                result.faithfulness_score
                for result in turn_results
            ),
        )

    def _calculate_average_answer_relevancy_score(
        self,
        *,
        turn_results: tuple[TurnRAGResult, ...],
    ) -> float:
        return self._average_calculator.calculate(
            values=tuple(
                result.answer_relevancy_score
                for result in turn_results
            ),
        )

    def _calculate_average_context_precision_score(
        self,
        *,
        turn_results: tuple[TurnRAGResult, ...],
    ) -> float:
        return self._average_calculator.calculate(
            values=tuple(
                result.context_precision_score
                for result in turn_results
            ),
        )