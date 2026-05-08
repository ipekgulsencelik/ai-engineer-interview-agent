from src.domain.coverage.interview_coverage import InterviewCoverage


def test_interview_coverage_checks_existing_values() -> None:
    coverage = InterviewCoverage(
        covered_categories={"RAG"},
        covered_levels={"JR"},
        covered_question_types={"conceptual"},
    )

    assert coverage.has_category("RAG") is True
    assert coverage.has_level("JR") is True
    assert coverage.has_question_type("conceptual") is True


def test_interview_coverage_returns_false_for_missing_values() -> None:
    coverage = InterviewCoverage()

    assert coverage.has_category("RAG") is False
    assert coverage.has_level("JR") is False
    assert coverage.has_question_type("conceptual") is False
