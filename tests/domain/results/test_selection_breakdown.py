import pytest

from src.domain.results.selection_breakdown import SelectionBreakdown


def build_valid_breakdown(**overrides) -> SelectionBreakdown:
    payload = {
        "level_score": 0.8,
        "market_score": 0.9,
        "cv_gap_score": 0.7,
        "difficulty_score": 0.6,
        "diversity_score": 0.5,
        "fatigue_score": 1.0,
        "final_score": 0.82,
    }

    payload.update(overrides)

    return SelectionBreakdown(**payload)


def test_selection_breakdown_can_be_created_with_valid_data() -> None:
    breakdown = build_valid_breakdown()

    assert breakdown.level_score == 0.8
    assert breakdown.market_score == 0.9
    assert breakdown.cv_gap_score == 0.7
    assert breakdown.difficulty_score == 0.6
    assert breakdown.diversity_score == 0.5
    assert breakdown.fatigue_score == 1.0
    assert breakdown.final_score == 0.82


def test_selection_breakdown_is_immutable() -> None:
    breakdown = build_valid_breakdown()

    with pytest.raises(Exception):
        breakdown.level_score = 0.1


@pytest.mark.parametrize(
    "field_name",
    [
        "level_score",
        "market_score",
        "cv_gap_score",
        "difficulty_score",
        "diversity_score",
        "fatigue_score",
    ],
)
def test_normalized_scores_cannot_be_below_zero(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be greater than or equal to 0.0",
    ):
        build_valid_breakdown(
            **{
                field_name: -0.1,
            }
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "level_score",
        "market_score",
        "cv_gap_score",
        "difficulty_score",
        "diversity_score",
        "fatigue_score",
    ],
)
def test_normalized_scores_cannot_be_above_one(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be less than or equal to 1.0",
    ):
        build_valid_breakdown(
            **{
                field_name: 1.1,
            }
        )


def test_final_score_can_be_above_one() -> None:
    breakdown = build_valid_breakdown(
        final_score=1.75,
    )

    assert breakdown.final_score == 1.75


def test_final_score_cannot_be_negative() -> None:
    with pytest.raises(
        ValueError,
        match="final_score must be greater than or equal to 0.0",
    ):
        build_valid_breakdown(
            final_score=-0.1,
        )