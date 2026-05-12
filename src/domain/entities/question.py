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


@dataclass(frozen=True)
class Question:
    """
    Interview sisteminde adaya sorulabilecek tek bir soruyu temsil eden
    immutable domain entity.

    Bu entity yalnızca domain state taşır.

    Sorumlulukları:
        - question bilgisini immutable şekilde temsil etmek
        - oluşturulduktan sonra domain invariant validation tetiklemek

    Bu entity şunları yapmaz:
        - raw string parse etmez
        - normalization yapmaz
        - JSON okumaz
        - repository işlemi yapmaz
        - scoring hesaplamaz
        - selection kararı vermez

    Raw input conversion ve normalization:
        QuestionFactory + QuestionFieldParser tarafından yapılır.

    Validation:
        QuestionValidator tarafından yapılır.
    """

    id: str
    text: str
    category: QuestionCategory
    level: Level
    difficulty: int
    question_type: QuestionType
    expected_points: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    market_weight: float = DEFAULT_MARKET_WEIGHT
    followup_allowed: bool = DEFAULT_FOLLOWUP_ALLOWED

    def __post_init__(self) -> None:
        """
        Entity oluşturulduktan sonra invariant validation çalıştırılır.
        """

        QuestionValidator.validate(self)