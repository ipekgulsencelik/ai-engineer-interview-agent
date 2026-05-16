from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.constants.question import (
    DEFAULT_FOLLOWUP_ALLOWED,
    DEFAULT_MARKET_WEIGHT,
)
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.validators.question_validator import QuestionValidator


@dataclass(frozen=True, slots=True)
class Question:
    """
    Interview sisteminde adaya sorulabilecek tek bir soruyu temsil eden
    immutable domain entity.

    Bu entity:
        - yalnızca domain state taşır
        - raw input parse etmez
        - normalization yapmaz
        - JSON/payload okumaz
        - repository işlemi yapmaz
        - scoring hesaplamaz
        - selection kararı vermez

    Validation kuralları:
        QUESTION_VALIDATION_SCHEMA üzerinden QuestionValidator tarafından uygulanır.
    """

    id: str
    text: str
    category: QuestionCategory
    level: Level
    difficulty: int
    question_type: QuestionType
    expected_points: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    followup: str | None = None
    ideal_answer_hint: str | None = None
    market_weight: float = DEFAULT_MARKET_WEIGHT
    followup_allowed: bool = DEFAULT_FOLLOWUP_ALLOWED

    def __post_init__(self) -> None:
        """
        Entity oluşturulduktan sonra domain invariant validation çalıştırılır.
        """

        QuestionValidator.validate(self)