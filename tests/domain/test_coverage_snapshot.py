from src.domain.coverage.coverage_snapshot import CoverageSnapshot


def test_coverage_snapshot_total_questions_returns_category_sum() -> None:
    snapshot = CoverageSnapshot(
        category_counts={"RAG": 2, "LLM Evaluation": 1},
        level_counts={"JR": 1, "MID": 2},
        question_type_counts={"conceptual": 3},
    )

    assert snapshot.total_questions == 3


def test_coverage_snapshot_can_be_created_with_defaults() -> None:
    snapshot = CoverageSnapshot()

    assert snapshot.category_counts == {}
    assert snapshot.level_counts == {}
    assert snapshot.question_type_counts == {}
    assert snapshot.total_questions == 0
