from src.domain.scoring.semantic_diversity import (
    compute_semantic_diversity_score,
)


def test_semantic_diversity_returns_one_when_similarity_unknown() -> None:
    score = compute_semantic_diversity_score(None)

    assert score == 1.0


def test_semantic_diversity_penalizes_high_similarity() -> None:
    score = compute_semantic_diversity_score(0.92)

    assert score == 0.60


def test_semantic_diversity_penalizes_moderate_similarity() -> None:
    score = compute_semantic_diversity_score(0.75)

    assert score == 0.85


def test_semantic_diversity_returns_one_for_healthy_diversity() -> None:
    score = compute_semantic_diversity_score(0.40)

    assert score == 1.0
