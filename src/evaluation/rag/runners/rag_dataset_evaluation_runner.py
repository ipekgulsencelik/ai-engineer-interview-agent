from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.rag.builders.rag_evaluation_report_builder import (
    RAGEvaluationReportBuilder,
)
from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)
from src.evaluation.rag.factories.rag_dataset_run_result_factory import (
    RAGDatasetRunResultFactory,
)
from src.evaluation.rag.services.rag_sample_evaluation_service import (
    RAGSampleEvaluationService,
)
from src.evaluation.rag.validators.rag_dataset_evaluation_input_validator import (
    RAGDatasetEvaluationInputValidator,
)
from src.evaluation.rag.value_objects.rag_dataset_run_result import (
    RAGDatasetRunResult,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGDatasetEvaluationRunner:
    """
    Dataset-level RAG evaluation runner.

    Orchestrates evaluation over all dataset samples
    and builds a dataset-level run result.
    """

    def __init__(
        self,
        *,
        sample_evaluation_service: (
            RAGSampleEvaluationService | None
        ) = None,
        report_builder: (
            RAGEvaluationReportBuilder | None
        ) = None,
        run_result_factory: (
            RAGDatasetRunResultFactory | None
        ) = None,
        input_validator: (
            RAGDatasetEvaluationInputValidator | None
        ) = None,
    ) -> None:
        self._sample_evaluation_service = (
            sample_evaluation_service
            or RAGSampleEvaluationService()
        )
        self._report_builder = (
            report_builder
            or RAGEvaluationReportBuilder()
        )
        self._run_result_factory = (
            run_result_factory
            or RAGDatasetRunResultFactory()
        )
        self._input_validator = (
            input_validator
            or RAGDatasetEvaluationInputValidator()
        )

    def run(
        self,
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        samples: tuple[
            RAGEvaluationSample,
            ...,
        ],
        generated_answers: dict[
            str,
            str,
        ],
        retrieved_contexts: dict[
            str,
            str,
        ],
        retrieved_chunk_ids: dict[
            str,
            tuple[
                str,
                ...,
            ],
        ] | None = None,
        notes: str | None = None,
    ) -> RAGDatasetRunResult:
        self._input_validator.validate(
            samples=samples,
            generated_answers=generated_answers,
            retrieved_contexts=retrieved_contexts,
        )

        started_at = datetime.now(
            UTC,
        )

        results = self._evaluate_samples(
            experiment_id=experiment_id,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            samples=samples,
            generated_answers=generated_answers,
            retrieved_contexts=retrieved_contexts,
            retrieved_chunk_ids=(
                retrieved_chunk_ids
                or {}
            ),
        )

        completed_at = datetime.now(
            UTC,
        )

        return self._build_run_result(
            experiment_id=experiment_id,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            samples=samples,
            results=results,
            started_at=started_at,
            completed_at=completed_at,
            notes=notes,
        )

    def _evaluate_samples(
        self,
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        samples: tuple[
            RAGEvaluationSample,
            ...,
        ],
        generated_answers: dict[
            str,
            str,
        ],
        retrieved_contexts: dict[
            str,
            str,
        ],
        retrieved_chunk_ids: dict[
            str,
            tuple[
                str,
                ...,
            ],
        ],
    ) -> tuple[
        RAGEvaluationResult,
        ...,
    ]:
        return tuple(
            self._sample_evaluation_service.evaluate(
                experiment_id=experiment_id,
                model_name=model_name,
                retriever_name=retriever_name,
                evaluator_name=evaluator_name,
                sample=sample,
                generated_answer=generated_answers[
                    sample.sample_id
                ],
                retrieved_context=retrieved_contexts[
                    sample.sample_id
                ],
                retrieved_chunk_ids=(
                    retrieved_chunk_ids.get(
                        sample.sample_id,
                        (),
                    )
                ),
            )
            for sample in samples
        )

    def _build_run_result(
        self,
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        samples: tuple[
            RAGEvaluationSample,
            ...,
        ],
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
        started_at: datetime,
        completed_at: datetime,
        notes: str | None,
    ) -> RAGDatasetRunResult:
        first_sample = samples[0]

        report = self._report_builder.build(
            experiment_id=experiment_id,
            benchmark_id=first_sample.benchmark_id,
            benchmark_name=first_sample.benchmark_name,
            benchmark_version=first_sample.benchmark_version,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            results=results,
            generated_at=completed_at,
            notes=notes,
        )

        return self._run_result_factory.create(
            experiment_id=experiment_id,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            report=report,
            started_at=started_at,
            completed_at=completed_at,
            notes=notes,
        )