from __future__ import annotations

from src.evaluation.rag.evaluators.rag_pass_fail_evaluator import RAGPassFailEvaluator


def test_rag_pass_fail_evaluator_should_pass_when_all_thresholds_are_met() -> None:
    assert RAGPassFailEvaluator.evaluate(
        retrieval_precision=1.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=False,
    ) is True


def test_rag_pass_fail_evaluator_should_fail_when_hallucination_is_detected() -> None:
    assert RAGPassFailEvaluator.evaluate(
        retrieval_precision=1.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=True,
    ) is False
