from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.enums.hallucination_label import (
    HallucinationLabel,
)
from src.evaluation.rag.validators.hallucination_result_validator import (
    HallucinationResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class HallucinationResult:
    """
    Immutable hallucination detection result.

    Represents hallucination analysis for a generated
    answer relative to retrieved evidence.
    """

    label: HallucinationLabel

    confidence: float

    hallucination_score: float

    hallucination_detected: bool

    unsupported_claim_count: int

    total_claim_count: int

    explanation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        HallucinationResultValidator.validate(
            label=self.label,
            confidence=self.confidence,
            hallucination_score=(
                self.hallucination_score
            ),
            hallucination_detected=(
                self.hallucination_detected
            ),
            unsupported_claim_count=(
                self.unsupported_claim_count
            ),
            total_claim_count=(
                self.total_claim_count
            ),
            explanation=self.explanation,
            notes=self.notes,
        )

    @property
    def unsupported_claim_rate(
        self,
    ) -> float:
        if self.total_claim_count == 0:
            return 0.0

        return (
            self.unsupported_claim_count
            / self.total_claim_count
        )

    @property
    def is_safe(
        self,
    ) -> bool:
        return not self.hallucination_detected

    @property
    def is_high_risk(
        self,
    ) -> bool:
        return self.label in {
            HallucinationLabel.HIGH,
            HallucinationLabel.CRITICAL,
        }

    @property
    def has_unsupported_claims(
        self,
    ) -> bool:
        return (
            self.unsupported_claim_count > 0
        )