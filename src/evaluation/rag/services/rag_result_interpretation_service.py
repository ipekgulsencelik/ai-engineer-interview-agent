from __future__ import annotations

from src.evaluation.rag.calculators.rag_overall_score_calculator import (
    RAGOverallScoreCalculator,
)
from src.evaluation.rag.detectors.hallucination_detector import (
    HallucinationDetector,
)
from src.evaluation.rag.evaluators.rag_pass_fail_evaluator import (
    RAGPassFailEvaluator,
)
from src.evaluation.rag.interpreters.rag_metric_interpreter import (
    RAGMetricInterpreter,
)
from src.evaluation.rag.value_objects.rag_evaluation_outcome import (
    RAGEvaluationOutcome,
)
from src.evaluation.rag.value_objects.rag_metric_evaluation_result import (
    RAGMetricEvaluationResult,
)
from src.evaluation.rag.value_objects.rag_retrieval_metric_result import (
    RAGRetrievalMetricResult,
)


class RAGResultInterpretationService:
    """
    Calculates final RAG outcome from metric results.
    """

    def __init__(
        self,
        *,
        overall_score_calculator: (
            RAGOverallScoreCalculator | None
        ) = None,
        hallucination_detector: HallucinationDetector | None = None,
        pass_fail_evaluator: RAGPassFailEvaluator | None = None,
        metric_interpreter: RAGMetricInterpreter | None = None,
    ) -> None:
        self._overall_score_calculator = (
            overall_score_calculator
            or RAGOverallScoreCalculator()
        )
        self._hallucination_detector = (
            hallucination_detector or HallucinationDetector()
        )
        self._pass_fail_evaluator = (
            pass_fail_evaluator or RAGPassFailEvaluator()
        )
        self._metric_interpreter = (
            metric_interpreter or RAGMetricInterpreter()
        )

    def evaluate(
        self,
        *,
        metric_result: RAGMetricEvaluationResult,
        retrieval_result: RAGRetrievalMetricResult,
    ) -> RAGEvaluationOutcome:
        overall_score = self._calculate_overall_score(
            metric_result=metric_result,
            retrieval_result=retrieval_result,
        )

        hallucination_detected = (
            self._hallucination_detector.detect(
                faithfulness_score=(
                    metric_result.faithfulness_score
                ),
            )
        )

        passed = self._evaluate_pass_fail(
            metric_result=metric_result,
            retrieval_result=retrieval_result,
            overall_score=overall_score,
            hallucination_detected=hallucination_detected,
        )

        interpretation = self._interpret(
            metric_result=metric_result,
            retrieval_result=retrieval_result,
            overall_score=overall_score,
            hallucination_detected=hallucination_detected,
        )

        return RAGEvaluationOutcome(
            overall_score=overall_score,
            hallucination_detected=hallucination_detected,
            passed=passed,
            interpretation=interpretation,
        )

    def _calculate_overall_score(
        self,
        *,
        metric_result: RAGMetricEvaluationResult,
        retrieval_result: RAGRetrievalMetricResult,
    ) -> float:
        return self._overall_score_calculator.calculate(
            retrieval_precision=(
                retrieval_result.retrieval_precision
            ),
            retrieval_recall=retrieval_result.retrieval_recall,
            context_relevance_score=(
                metric_result.context_relevance_score
            ),
            faithfulness_score=(
                metric_result.faithfulness_score
            ),
            answer_relevance_score=(
                metric_result.answer_relevance_score
            ),
            answer_correctness_score=(
                metric_result.answer_correctness_score
            ),
        )

    def _evaluate_pass_fail(
        self,
        *,
        metric_result: RAGMetricEvaluationResult,
        retrieval_result: RAGRetrievalMetricResult,
        overall_score: float,
        hallucination_detected: bool,
    ) -> bool:
        return self._pass_fail_evaluator.evaluate(
            retrieval_precision=(
                retrieval_result.retrieval_precision
            ),
            retrieval_recall=retrieval_result.retrieval_recall,
            context_relevance_score=(
                metric_result.context_relevance_score
            ),
            faithfulness_score=(
                metric_result.faithfulness_score
            ),
            answer_relevance_score=(
                metric_result.answer_relevance_score
            ),
            answer_correctness_score=(
                metric_result.answer_correctness_score
            ),
            overall_score=overall_score,
            hallucination_detected=hallucination_detected,
        )

    def _interpret(
        self,
        *,
        metric_result: RAGMetricEvaluationResult,
        retrieval_result: RAGRetrievalMetricResult,
        overall_score: float,
        hallucination_detected: bool,
    ) -> str:
        return self._metric_interpreter.interpret(
            retrieval_precision=(
                retrieval_result.retrieval_precision
            ),
            retrieval_recall=retrieval_result.retrieval_recall,
            context_relevance_score=(
                metric_result.context_relevance_score
            ),
            faithfulness_score=(
                metric_result.faithfulness_score
            ),
            answer_relevance_score=(
                metric_result.answer_relevance_score
            ),
            answer_correctness_score=(
                metric_result.answer_correctness_score
            ),
            overall_score=overall_score,
            hallucination_detected=hallucination_detected,
        )