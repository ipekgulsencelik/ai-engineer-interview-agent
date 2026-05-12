import pytest

from src.domain.scoring.scoring_weights import ScoringWeights


def build_weights(**overrides) -> ScoringWeights:
    payload = {
        "level_weight": 1.0,
        "market_weight": 1.0,
        "cv_gap_weight": 1.0,
        "difficulty_weight": 1.0,
        "diversity_weight": 1.0,
        "fatigue_weight": 1.0,
        "semantic_relevance_weight": 1.0,
    }

    payload.update(overrides)

    return ScoringWeights(**payload)


def test_scoring_weights_can_be_created_with_default_values() -> None:
    weights = ScoringWeights()

    assert weights.level_weight == 1.0
    assert weights.market_weight == 1.0
    assert weights.cv_gap_weight == 1.0
    assert weights.difficulty_weight == 1.0
    assert weights.diversity_weight == 1.0
    assert weights.fatigue_weight == 1.0
    assert weights.semantic_relevance_weight == 1.0


def test_scoring_weights_can_be_created_with_custom_values() -> None:
    weights = build_weights(
        market_weight=1.5,
        fatigue_weight=0.8,
    )

    assert weights.market_weight == 1.5
    assert weights.fatigue_weight == 0.8


def test_scoring_weights_is_immutable() -> None:
    weights = ScoringWeights()

    with pytest.raises(Exception):
        weights.market_weight = 2.0


@pytest.mark.parametrize(
    "field_name",
    [
        "level_weight",
        "market_weight",
        "cv_gap_weight",
        "difficulty_weight",
        "diversity_weight",
        "fatigue_weight",
        "semantic_relevance_weight",
    ],
)
def test_scoring_weights_cannot_be_negative(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be greater than or equal to 0.0",
    ):
        build_weights(
            **{
                field_name: -0.1,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("level_weight", "1.0"),
        ("market_weight", []),
        ("cv_gap_weight", object()),
        ("difficulty_weight", None),
    ],
)
def test_scoring_weights_rejects_invalid_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_weights(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "level_weight",
        "market_weight",
        "cv_gap_weight",
        "difficulty_weight",
        "diversity_weight",
        "fatigue_weight",
        "semantic_relevance_weight",
    ],
)
def test_scoring_weights_rejects_bool_values(
    field_name: str,
) -> None:
    with pytest.raises(TypeError):
        build_weights(
            **{
                field_name: True,
            }
        )


@pytest.mark.parametrize(
    "value",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_scoring_weights_rejects_non_finite_values(
    value: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="market_weight must be finite",
    ):
        build_weights(
            market_weight=value,
        )