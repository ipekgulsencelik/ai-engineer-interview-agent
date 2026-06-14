from __future__ import annotations

import pytest

from src.evaluation.rag.calculators.rag_overall_score_calculator import RAGOverallScoreCalculator


def test_rag_overall_score_should_average_all_sample_level_components() -> None:
    assert RAGOverallScoreCalculator().calculate(
        retrieval_precision=1.0,
        retrieval_recall=0.5,
        context_relevance_score=0.5,
        faithfulness_score=1.0,
        answer_relevance_score=0.5,
        answer_correctness_score=0.5,
    ) == pytest.approx(4 / 6)
