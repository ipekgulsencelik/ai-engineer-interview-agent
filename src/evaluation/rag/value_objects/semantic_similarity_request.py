from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.semantic_similarity_request_validator import (
    SemanticSimilarityRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class SemanticSimilarityRequest:
    """
    Request model for semantic similarity evaluation.
    """

    reference_text: str

    candidate_text: str

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        SemanticSimilarityRequestValidator.validate(
            reference_text=self.reference_text,
            candidate_text=self.candidate_text,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )