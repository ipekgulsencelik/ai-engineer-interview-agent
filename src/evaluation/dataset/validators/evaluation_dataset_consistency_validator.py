from __future__ import annotations

from typing import Protocol

from src.evaluation.domain.entities import (
    EvaluationSample,
    HumanScore,
    LLMScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class SampleReference(Protocol):
    sample_id: str


class EvaluationDatasetConsistencyValidator:
    """
    Cross-entity consistency validation service.

    Ensures that all evaluation-related entities
    reference valid EvaluationSample instances.
    """

    @classmethod
    def validate(
        cls,
        *,
        samples: tuple[EvaluationSample, ...],
        human_scores: tuple[HumanScore, ...] = (),
        llm_scores: tuple[LLMScore, ...] = (),
    ) -> None:
        sample_ids = frozenset(
            sample.sample_id
            for sample in samples
        )

        cls._validate_references(
            sample_ids=sample_ids,
            entity_name="HumanScore",
            references=human_scores,
        )

        cls._validate_references(
            sample_ids=sample_ids,
            entity_name="LLMScore",
            references=llm_scores,
        )

    @staticmethod
    def _validate_references(
        *,
        sample_ids: frozenset[str],
        entity_name: str,
        references: tuple[SampleReference, ...],
    ) -> None:
        for reference in references:
            if reference.sample_id not in sample_ids:
                raise EvaluationValidationError(
                    f"{entity_name} references unknown "
                    f"sample_id: {reference.sample_id}"
                )