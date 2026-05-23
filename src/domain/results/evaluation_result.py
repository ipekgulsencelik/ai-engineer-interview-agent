from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.constants.evaluation import (
    DEFAULT_COMMUNICATION_SCORE,
    DEFAULT_DEPTH_SCORE,
    DEFAULT_TECHNICAL_ACCURACY_SCORE,
)
from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.validators.evaluation_result_validator import (
    EvaluationResultValidator,
)


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """
    Structured answer evaluation result model.
    """

    score: float

    feedback: str

    technical_accuracy: float = (
        DEFAULT_TECHNICAL_ACCURACY_SCORE
    )

    depth: float = (
        DEFAULT_DEPTH_SCORE
    )

    communication: float = (
        DEFAULT_COMMUNICATION_SCORE
    )

    metadata: EvaluationMetadata = field(
        default_factory=EvaluationMetadata,
    )

    def __post_init__(self) -> None:
        EvaluationResultValidator.validate(
            self,
        )