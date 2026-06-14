from __future__ import annotations

from datetime import datetime

from src.evaluation.rag.aggregators.rag_metrics_aggregator import (
    RAGMetricsAggregator,
)
from src.evaluation.rag.calculators.rag_rate_calculator import (
    RAGRateCalculator,
)
from src.evaluation.rag.calculators.rag_report_count_calculator import (
    RAGReportCountCalculator,
)
from src.evaluation.rag.entities.rag_evaluation_report import (
    RAGEvaluationReport,
)
from src.evaluation.rag.factories.rag_evaluation_report_factory import (
    RAGEvaluationReportFactory,
)
from src.evaluation.rag.interpreters.rag_report_interpreter import (
    RAGReportInterpreter,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGEvaluationReportBuilder:
    """
    Builds aggregated RAG evaluation reports.
    """

    def __init__(
        self,
        *,
        metrics_aggregator: RAGMetricsAggregator | None = None,
        rate_calculator: RAGRateCalculator | None = None,
        count_calculator: RAGReportCountCalculator | None = None,
        interpreter: RAGReportInterpreter | None = None,
        report_factory: RAGEvaluationReportFactory | None = None,
    ) -> None:
        self._metrics_aggregator = (
            metrics_aggregator
            or RAGMetricsAggregator()
        )
        self._rate_calculator = (
            rate_calculator
            or RAGRateCalculator()
        )
        self._count_calculator = (
            count_calculator
            or RAGReportCountCalculator()
        )
        self._interpreter = (
            interpreter
            or RAGReportInterpreter()
        )
        self._report_factory = (
            report_factory
            or RAGEvaluationReportFactory()
        )

    def build(
        self,
        *,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
        generated_at: datetime | None = None,
        notes: str | None = None,
    ) -> RAGEvaluationReport:
        metrics = self._metrics_aggregator.aggregate(
            results=results,
        )

        sample_count = (
            self._count_calculator.sample_count(
                results=results,
            )
        )

        hallucination_count = (
            self._count_calculator.hallucination_count(
                results=results,
            )
        )

        passed_count = (
            self._count_calculator.passed_count(
                results=results,
            )
        )

        failed_count = (
            self._count_calculator.failed_count(
                results=results,
            )
        )

        hallucination_rate = (
            self._rate_calculator.calculate(
                numerator=hallucination_count,
                denominator=sample_count,
            )
        )

        pass_rate = (
            self._rate_calculator.calculate(
                numerator=passed_count,
                denominator=sample_count,
            )
        )

        interpretation = (
            self._interpreter.interpret(
                sample_count=sample_count,
                failed_count=failed_count,
            )
        )

        return self._report_factory.create(
            experiment_id=experiment_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            results=results,
            sample_count=sample_count,
            average_retrieval_precision=(
                metrics.average_retrieval_precision
            ),
            average_retrieval_recall=(
                metrics.average_retrieval_recall
            ),
            average_context_relevance_score=(
                metrics.average_context_relevance_score
            ),
            average_faithfulness_score=(
                metrics.average_faithfulness_score
            ),
            average_answer_relevance_score=(
                metrics.average_answer_relevance_score
            ),
            average_answer_correctness_score=(
                metrics.average_answer_correctness_score
            ),
            average_overall_score=(
                metrics.average_overall_score
            ),
            hallucination_count=hallucination_count,
            hallucination_rate=hallucination_rate,
            passed_count=passed_count,
            failed_count=failed_count,
            pass_rate=pass_rate,
            interpretation=interpretation,
            generated_at=generated_at,
            notes=notes,
        )