from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.scoring.scoring_context import ScoringContext


def compute_level_score(
    *,
    question: Question,
    context: ScoringContext,
) -> float:
    """
    Question level ile current interview level uyumunu hesaplar.

    Exact match:
        1.0

    Bir seviye fark:
        0.6

    İki seviye fark:
        0.2
    """

    level_distance = abs(
        _level_rank(question.level) - _level_rank(context.current_level)
    )

    if level_distance == 0:
        return 1.0

    if level_distance == 1:
        return 0.6

    return 0.2


def compute_market_score(
    *,
    question: Question,
) -> float:
    """
    Question içindeki market_weight değerini market score olarak kullanır.
    """

    return question.market_weight


def compute_cv_gap_score(
    *,
    question: Question,
    context: ScoringContext,
) -> float:
    """
    Candidate CV'sinde question category ile ilişkili skill yoksa
    daha yüksek gap score üretir.

    Amaç:
        Candidate'ın eksik alanlarını probe etmek.
    """

    if not context.cv_skills:
        return 1.0

    normalized_category = question.category.value.lower()

    normalized_skills = [
        skill.lower().strip()
        for skill in context.cv_skills
    ]

    has_related_skill = any(
        normalized_category in skill
        or skill in normalized_category
        for skill in normalized_skills
    )

    if has_related_skill:
        return 0.2

    return 1.0


def compute_difficulty_score(
    *,
    question: Question,
    context: ScoringContext,
) -> float:
    """
    Recent performance'a göre difficulty suitability hesaplar.

    Recent score yoksa neutral score döner.
    """

    if not context.recent_scores:
        return 0.7

    average_score = sum(context.recent_scores) / len(context.recent_scores)

    if average_score >= 8.0:
        return _score_high_performance_difficulty(question.difficulty)

    if average_score <= 4.0:
        return _score_low_performance_difficulty(question.difficulty)

    return _score_mid_performance_difficulty(question.difficulty)


def compute_diversity_score(
    *,
    question: Question,
    context: ScoringContext,
) -> float:
    """
    Daha önce sorulmamış question'lara yüksek diversity score verir.
    """

    if question.id in context.asked_question_ids:
        return 0.0

    return 1.0


def compute_fatigue_score(
    *,
    context: ScoringContext,
) -> float:
    """
    Advanced fatigue signal yoksa neutral score döner.

    Eğer fatigue signal içinde fatigue_multiplier varsa onu kullanır.
    """

    fatigue = context.signals.fatigue

    if fatigue is None:
        return 1.0

    fatigue_multiplier = getattr(
        fatigue,
        "fatigue_multiplier",
        None,
    )

    if fatigue_multiplier is None:
        return 1.0

    return fatigue_multiplier


def _level_rank(
    level: Level,
) -> int:
    level_order = {
        Level.JR: 1,
        Level.MID: 2,
        Level.SENIOR: 3,
    }

    return level_order[level]


def _score_high_performance_difficulty(
    difficulty: int,
) -> float:
    if difficulty == 3:
        return 1.0

    if difficulty == 2:
        return 0.8

    return 0.5


def _score_mid_performance_difficulty(
    difficulty: int,
) -> float:
    if difficulty == 2:
        return 1.0

    if difficulty == 1:
        return 0.8

    return 0.7


def _score_low_performance_difficulty(
    difficulty: int,
) -> float:
    if difficulty == 1:
        return 1.0

    if difficulty == 2:
        return 0.6

    return 0.3