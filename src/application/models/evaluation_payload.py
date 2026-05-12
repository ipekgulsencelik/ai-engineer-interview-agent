from __future__ import annotations

from dataclasses import dataclass, field

from src.application.validators.evaluation_payload_validator import (
    EvaluationPayloadValidator,
)


@dataclass(frozen=True)
class EvaluationPayload:
    """
    Raw evaluator/provider çıktısından normalize edilmiş application payload.

    Bu model:
        - raw provider response ile domain result arasında ara schema görevi görür
        - domain result değildir
        - business fallback uygulamaz
        - invariant enforcement yapmaz

    Business fallback ve domain-safe creation:
        EvaluationResultFactory tarafında yapılır.
    """

    score: float | None = field(
        default=None,
        metadata={
            "type": (int, float),
            "nullable": True,
            "finite": True,
        },
    )

    feedback: str | None = field(
        default=None,
        metadata={
            "type": str,
            "nullable": True,
            "non_empty": True,
            "strip": True,
        },
    )

    technical_accuracy: float | None = field(
        default=None,
        metadata={
            "type": (int, float),
            "nullable": True,
            "finite": True,
        },
    )

    depth: float | None = field(
        default=None,
        metadata={
            "type": (int, float),
            "nullable": True,
            "finite": True,
        },
    )

    communication: float | None = field(
        default=None,
        metadata={
            "type": (int, float),
            "nullable": True,
            "finite": True,
        },
    )

    missing_keywords: tuple[str, ...] | None = field(
        default=None,
        metadata={
            "type": tuple,
            "nullable": True,
            "item_type": str,
        },
    )

    follow_up_question: str | None = field(
        default=None,
        metadata={
            "type": str,
            "nullable": True,
            "non_empty": True,
            "strip": True,
        },
    )

    confidence: float | None = field(
        default=None,
        metadata={
            "type": (int, float),
            "nullable": True,
            "finite": True,
        },
    )

    rubric_version: str | None = field(
        default=None,
        metadata={
            "type": str,
            "nullable": True,
            "non_empty": True,
            "strip": True,
        },
    )

    def __post_init__(self) -> None:
        EvaluationPayloadValidator.validate(self)