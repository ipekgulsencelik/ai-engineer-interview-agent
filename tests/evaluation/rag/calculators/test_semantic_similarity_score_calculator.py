from __future__ import annotations

from src.evaluation.rag.calculators.semantic_similarity_score_calculator import SemanticSimilarityScoreCalculator


def test_semantic_similarity_score_should_use_reference_tokens_as_denominator() -> None:
    assert SemanticSimilarityScoreCalculator().calculate(
        reference_tokens={"same", "idea"},
        candidate_tokens={"same"},
    ) == 0.5
