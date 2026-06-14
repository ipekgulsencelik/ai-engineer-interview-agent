from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.constants.rag_validation_constants import (
    FLOAT_COMPARISON_TOLERANCE,
)
from src.evaluation.rag.constants.rag_validation_messages import (
    HALLUCINATION_COUNT_EXCEEDED,
    HALLUCINATION_RATE_MISMATCH,
    INVALID_RESULT_ITEM,
    PASS_FAIL_COUNT_MISMATCH,
    PASS_RATE_MISMATCH,
    RESULTS_MUST_BE_TUPLE,
    SAMPLE_COUNT_MISMATCH,
)
from src.evaluation.rag.schemas.rag_evaluation_report_schema import (
    RAG_EVALUATION_REPORT_SCHEMA,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGEvaluationReportValidator:
    """
    RAGEvaluationReport validation service.
    """

    @staticmethod
    def validate(
        *,
        report_id: str,
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
        sample_count: int,
        average_retrieval_precision: float,
        average_retrieval_recall: float,
        average_context_relevance_score: float,
        average_faithfulness_score: float,
        average_answer_relevance_score: float,
        average_answer_correctness_score: float,
        average_overall_score: float,
        hallucination_count: int,
        hallucination_rate: float,
        passed_count: int,
        failed_count: int,
        pass_rate: float,
        generated_at: datetime,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "report_id": report_id,
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "results": results,
                "sample_count": sample_count,
                "average_retrieval_precision": (
                    average_retrieval_precision
                ),
                "average_retrieval_recall": (
                    average_retrieval_recall
                ),
                "average_context_relevance_score": (
                    average_context_relevance_score
                ),
                "average_faithfulness_score": (
                    average_faithfulness_score
                ),
                "average_answer_relevance_score": (
                    average_answer_relevance_score
                ),
                "average_answer_correctness_score": (
                    average_answer_correctness_score
                ),
                "average_overall_score": (
                    average_overall_score
                ),
                "hallucination_count": hallucination_count,
                "hallucination_rate": hallucination_rate,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "pass_rate": pass_rate,
                "generated_at": generated_at,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=RAG_EVALUATION_REPORT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            results,
            tuple,
        ):
            raise EvaluationValidationError(
                RESULTS_MUST_BE_TUPLE
            )

        for index, result in enumerate(
            results,
        ):
            if not isinstance(
                result,
                RAGEvaluationResult,
            ):
                raise EvaluationValidationError(
                    INVALID_RESULT_ITEM.format(
                        index=index,
                    )
                )

        if sample_count != len(
            results,
        ):
            raise EvaluationValidationError(
                SAMPLE_COUNT_MISMATCH
            )

        if (
            passed_count
            + failed_count
            != sample_count
        ):
            raise EvaluationValidationError(
                PASS_FAIL_COUNT_MISMATCH
            )

        if hallucination_count > sample_count:
            raise EvaluationValidationError(
                HALLUCINATION_COUNT_EXCEEDED
            )

        expected_pass_rate = (
            0.0
            if sample_count == 0
            else passed_count / sample_count
        )

        if (
            abs(
                pass_rate
                - expected_pass_rate
            )
            > FLOAT_COMPARISON_TOLERANCE
        ):
            raise EvaluationValidationError(
                PASS_RATE_MISMATCH
            )

        expected_hallucination_rate = (
            0.0
            if sample_count == 0
            else hallucination_count
            / sample_count
        )

        if (
            abs(
                hallucination_rate
                - expected_hallucination_rate
            )
            > FLOAT_COMPARISON_TOLERANCE
        ):
            raise EvaluationValidationError(
                HALLUCINATION_RATE_MISMATCH
            )