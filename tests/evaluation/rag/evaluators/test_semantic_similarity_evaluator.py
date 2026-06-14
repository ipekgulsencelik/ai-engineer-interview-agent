from __future__ import annotations

from src.evaluation.rag.evaluators.semantic_similarity_evaluator import SemanticSimilarityEvaluator
from src.evaluation.rag.value_objects.semantic_similarity_request import SemanticSimilarityRequest


def test_semantic_similarity_evaluator_should_score_reference_candidate_overlap() -> None:
    assert SemanticSimilarityEvaluator().evaluate(
        request=SemanticSimilarityRequest(
            reference_text="alpha beta",
            candidate_text="alpha gamma",
        )
    ) == 0.5
