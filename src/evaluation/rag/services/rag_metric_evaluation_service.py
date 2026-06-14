from __future__ import annotations

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
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
from src.evaluation.rag.factories.rag_sample_request_factory import (
    RAGSampleRequestFactory,
)
from src.evaluation.rag.value_objects.rag_metric_evaluation_result import (
    RAGMetricEvaluationResult,
)


class RAGMetricEvaluationService:
    """
    Evaluates generation-side RAG metrics.
    """

    def __init__(
        self,
        *,
        request_factory: RAGSampleRequestFactory | None = None,
        faithfulness_evaluator: FaithfulnessEvaluator | None = None,
        answer_relevancy_evaluator: (
            AnswerRelevancyEvaluator | None
        ) = None,
        context_precision_evaluator: (
            ContextPrecisionEvaluator | None
        ) = None,
    ) -> None:
        self._request_factory = (
            request_factory or RAGSampleRequestFactory()
        )
        self._faithfulness_evaluator = (
            faithfulness_evaluator or FaithfulnessEvaluator()
        )
        self._answer_relevancy_evaluator = (
            answer_relevancy_evaluator
            or AnswerRelevancyEvaluator()
        )
        self._context_precision_evaluator = (
            context_precision_evaluator
            or ContextPrecisionEvaluator()
        )

    def evaluate(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> RAGMetricEvaluationResult:
        faithfulness_score = self._evaluate_faithfulness(
            sample=sample,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

        answer_relevance_score = (
            self._evaluate_answer_relevancy(
                sample=sample,
                generated_answer=generated_answer,
                model_name=model_name,
                evaluator_name=evaluator_name,
            )
        )

        context_precision_score = (
            self._evaluate_context_precision(
                sample=sample,
                generated_answer=generated_answer,
                retrieved_context=retrieved_context,
                model_name=model_name,
                evaluator_name=evaluator_name,
            )
        )

        return RAGMetricEvaluationResult(
            faithfulness_score=faithfulness_score,
            answer_relevance_score=answer_relevance_score,
            context_precision_score=context_precision_score,
        )

    def _evaluate_faithfulness(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> float:
        return self._faithfulness_evaluator.evaluate(
            request=self._request_factory.build_faithfulness_request(
                sample=sample,
                generated_answer=generated_answer,
                retrieved_context=retrieved_context,
                model_name=model_name,
                evaluator_name=evaluator_name,
            )
        )

    def _evaluate_answer_relevancy(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        model_name: str,
        evaluator_name: str,
    ) -> float:
        return self._answer_relevancy_evaluator.evaluate(
            request=(
                self._request_factory.build_answer_relevancy_request(
                    sample=sample,
                    generated_answer=generated_answer,
                    model_name=model_name,
                    evaluator_name=evaluator_name,
                )
            )
        )

    def _evaluate_context_precision(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> float:
        return self._context_precision_evaluator.evaluate(
            request=(
                self._request_factory.build_context_precision_request(
                    sample=sample,
                    generated_answer=generated_answer,
                    retrieved_context=retrieved_context,
                    model_name=model_name,
                    evaluator_name=evaluator_name,
                )
            )
        )