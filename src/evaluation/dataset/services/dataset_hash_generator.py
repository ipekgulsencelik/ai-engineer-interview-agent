from __future__ import annotations

import hashlib
import json

from src.evaluation.dataset.entities import (
    EvaluationDataset,
)


class DatasetHashGenerator:
    """
    Deterministic dataset fingerprint generator.
    """

    def generate(
        self,
        dataset: EvaluationDataset,
    ) -> str:
        serialized = self._serialize_dataset(
            dataset=dataset,
        )

        return hashlib.sha256(
            serialized.encode(
                "utf-8",
            )
        ).hexdigest()

    def _serialize_dataset(
        self,
        *,
        dataset: EvaluationDataset,
    ) -> str:
        payload = {
            "dataset_id": dataset.dataset_id,
            "dataset_name": dataset.dataset_name,
            "dataset_version": (
                dataset.dataset_version.version
            ),
            "dataset_stage": (
                dataset.dataset_version.stage.value
            ),
            "samples": [
                {
                    "sample_id": sample.sample_id,
                    "question_id": sample.question_id,
                    "question": sample.question,
                    "candidate_answer": (
                        sample.candidate_answer
                    ),
                    "expected_answer": (
                        sample.expected_answer
                    ),
                    "category": sample.category,
                    "level": sample.level.value,
                }
                for sample in dataset.samples
            ],
            "human_scores": [
                {
                    "sample_id": score.sample_id,
                    "evaluator_id": (
                        score.evaluator_id
                    ),
                    "overall_score": (
                        score.overall_score
                    ),
                    "technical_score": (
                        score.technical_score
                    ),
                    "communication_score": (
                        score.communication_score
                    ),
                }
                for score in dataset.human_scores
            ],
            "llm_scores": [
                {
                    "sample_id": score.sample_id,
                    "model_name": (
                        score.model_name
                    ),
                    "overall_score": (
                        score.overall_score
                    ),
                    "technical_score": (
                        score.technical_score
                    ),
                    "communication_score": (
                        score.communication_score
                    ),
                    "reasoning_score": (
                        score.reasoning_score
                    ),
                }
                for score in dataset.llm_scores
            ],
        }

        return json.dumps(
            payload,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
        )