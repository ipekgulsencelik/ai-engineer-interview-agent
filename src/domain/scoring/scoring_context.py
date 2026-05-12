from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from src.domain.enums.level import Level
from src.domain.parsers.scoring_context_field_parser import (
    ScoringContextFieldParser,
)
from src.domain.scoring.scoring_signals import (
    ScoringSignals,
)
from src.domain.validators.scoring_context_validator import (
    ScoringContextValidator,
)


@dataclass(frozen=True)
class ScoringContext:
    """
    Question scoring sürecinde kullanılan immutable runtime context modelidir.

    Bu model yalnızca scoring engine'in ihtiyaç duyduğu interview state
    snapshot'ını taşır.

    Bu model:
        - score hesaplamaz
        - ranking yapmaz
        - question seçmez
        - persistence işlemi yapmaz

    Validation:
        ScoringContextValidator tarafından yapılır.
    """

    current_level: Level | str = Level.JR

    cv_skills: tuple[str, ...] = field(
        default_factory=tuple,
    )

    asked_question_ids: frozenset[str] = field(
        default_factory=frozenset,
    )

    recent_scores: tuple[float, ...] = field(
        default_factory=tuple,
    )

    weak_areas: tuple[str, ...] = field(
        default_factory=tuple,
    )

    signals: ScoringSignals = field(
        default_factory=ScoringSignals,
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "current_level",
            ScoringContextFieldParser.parse_level(
                self.current_level,
            ),
        )

        ScoringContextValidator.validate(
            self,
        )