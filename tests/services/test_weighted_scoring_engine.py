from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.services.weighted_scoring_engine import (
    WeightedScoringEngine,
)


def make_question(level: str, market_weight: float) -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level=level,
        difficulty=1,
        question_type="conceptual",
        expected_points=[],
        keywords=[],
        market_weight=market_weight,
    )


def test_weighted_scoring_engine_prefers_matching_level() -> None:
    engine = WeightedScoringEngine()

    context = ScoringContext(current_level="JR")

    jr_question = make_question("JR", 0.5)
    senior_question = make_question("SENIOR", 0.5)

    jr_score = engine.score(jr_question, context)
    senior_score = engine.score(senior_question, context)

    assert jr_score > senior_score
