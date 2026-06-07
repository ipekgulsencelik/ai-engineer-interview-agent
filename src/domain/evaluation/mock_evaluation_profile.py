from dataclasses import dataclass, field

from src.domain.constants.evaluation import (
    DEFAULT_CONFIDENCE,
    DEFAULT_MOCK_COMMUNICATION,
    DEFAULT_MOCK_DEPTH,
    DEFAULT_MOCK_FEEDBACK,
    DEFAULT_MOCK_RUBRIC_VERSION,
    DEFAULT_MOCK_SCORE,
    DEFAULT_MOCK_TECHNICAL_ACCURACY,
    MAX_CONFIDENCE,
    MAX_EVALUATION_SCORE,
    MIN_CONFIDENCE,
    MIN_EVALUATION_SCORE,
    MIN_NORMALIZED_SCORE,
)


@dataclass(frozen=True)
class MockEvaluationProfile:

    score: float = field(
        default=DEFAULT_MOCK_SCORE,
        metadata={
            "type": (int, float),
            "finite": True,
            "min_value": MIN_NORMALIZED_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    feedback: str = field(
        default=DEFAULT_MOCK_FEEDBACK,
        metadata={
            "type": str,
            "non_empty": True,
            "strip": True,  
        },
    )

    technical_accuracy: float = field(
        default=DEFAULT_MOCK_TECHNICAL_ACCURACY,
        metadata={
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    depth: float = field(
        default=DEFAULT_MOCK_DEPTH,
        metadata={
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    communication: float = field(
        default=DEFAULT_MOCK_COMMUNICATION,
        metadata={
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    missing_keywords: list[str] = field(
        default_factory=list,
        metadata={
            "type": list,
            "item_type": str,
        },
    )

    follow_up_question: str | None = field(
        default=None,
        metadata={
            "nullable": True,
            "type": str,
            "strip": True,
        },
    )

    confidence: float = field(
        default=DEFAULT_CONFIDENCE,
        metadata={
            "type": (int, float),
            "finite": True,
            "min_value": MIN_CONFIDENCE,
            "max_value": MAX_CONFIDENCE,
        },
    )

    rubric_version: str = field(
        default=DEFAULT_MOCK_RUBRIC_VERSION,
        metadata={
            "type": str,
            "non_empty": True,
            "strip": True,
        },
    )

    def __post_init__(self) -> None:

        from src.domain.validators.mock_evaluation_profile_validator import (
            MockEvaluationProfileValidator,
        )

        MockEvaluationProfileValidator.validate(self)