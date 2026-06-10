from __future__ import annotations

from typing import Any

from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)


class EvaluationDatasetSerializer:
    """
    Serializes EvaluationDataset aggregates into JSON-safe dictionaries.
    """

    @classmethod
    def serialize(
        cls,
        *,
        dataset: EvaluationDataset,
    ) -> dict[str, Any]:
        return {
            "dataset_id": dataset.dataset_id,
            "dataset_name": dataset.dataset_name,
            "description": dataset.description,
            "dataset_version": cls._serialize_version(
                dataset=dataset,
            ),
            "metadata": cls._serialize_metadata(
                dataset=dataset,
            ),
            "samples": cls._serialize_samples(
                dataset=dataset,
            ),
            "human_scores": cls._serialize_human_scores(
                dataset=dataset,
            ),
            "llm_scores": cls._serialize_llm_scores(
                dataset=dataset,
            ),
        }

    @staticmethod
    def _serialize_version(
        *,
        dataset: EvaluationDataset,
    ) -> dict[str, Any]:
        return {
            "version": dataset.dataset_version.version,
            "stage": dataset.dataset_version.stage.value,
            "created_by": dataset.dataset_version.created_by,
            "description": dataset.dataset_version.description,
        }

    @staticmethod
    def _serialize_metadata(
        *,
        dataset: EvaluationDataset,
    ) -> dict[str, Any]:
        return {
            "created_at": dataset.metadata.created_at.isoformat(),
            "rubric_version": dataset.metadata.rubric_version,
            "evaluator_version": dataset.metadata.evaluator_version,
            "source": dataset.metadata.source,
            "notes": dataset.metadata.notes,
        }

    @staticmethod
    def _serialize_samples(
        *,
        dataset: EvaluationDataset,
    ) -> list[dict[str, Any]]:
        return [
            {
                "sample_id": sample.sample_id,
                "question_id": sample.question_id,
                "question": sample.question,
                "candidate_answer": sample.candidate_answer,
                "expected_answer": sample.expected_answer,
                "category": sample.category,
                "level": sample.level.value,
                "retrieved_contexts": list(
                    sample.retrieved_contexts,
                ),
                "metadata": sample.metadata,
            }
            for sample in dataset.samples
        ]

    @staticmethod
    def _serialize_human_scores(
        *,
        dataset: EvaluationDataset,
    ) -> list[dict[str, Any]]:
        return [
            {
                "sample_id": score.sample_id,
                "evaluator_id": score.evaluator_id,
                "overall_score": score.overall_score,
                "technical_score": score.technical_score,
                "communication_score": score.communication_score,
                "feedback": score.feedback,
            }
            for score in dataset.human_scores
        ]

    @staticmethod
    def _serialize_llm_scores(
        *,
        dataset: EvaluationDataset,
    ) -> list[dict[str, Any]]:
        return [
            {
                "sample_id": score.sample_id,
                "model_name": score.model_name,
                "overall_score": score.overall_score,
                "technical_score": score.technical_score,
                "communication_score": score.communication_score,
                "reasoning_score": score.reasoning_score,
                "confidence_score": score.confidence_score,
                "feedback": score.feedback,
            }
            for score in dataset.llm_scores
        ]