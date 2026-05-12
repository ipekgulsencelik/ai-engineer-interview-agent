from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.enums.level import Level
from src.domain.parsers.scoring_context_field_parser import (
    ScoringContextFieldParser,
)
from src.domain.scoring.scoring_signals import ScoringSignals
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
    cv_skills: list[str] = field(default_factory=list)
    asked_question_ids: list[str] = field(default_factory=list)
    recent_scores: list[float] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)
    signals: ScoringSignals = field(default_factory=ScoringSignals)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "current_level",
            ScoringContextFieldParser.parse_level(
                self.current_level,
            ),
        )

        ScoringContextValidator.validate(self)