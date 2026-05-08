from dataclasses import dataclass, field

from src.domain.enums.level import Level
from src.domain.enums.question_type import QuestionType
from src.domain.parsers.question_field_parser import QuestionFieldParser
from src.domain.validators.question_validator import QuestionValidator


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    category: str
    level: Level | str
    difficulty: int
    question_type: QuestionType | str
    expected_points: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    market_weight: float = 0.5
    followup_allowed: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "level",
            QuestionFieldParser.parse_level(self.level),
        )

        object.__setattr__(
            self,
            "question_type",
            QuestionFieldParser.parse_question_type(
                self.question_type,
            ),
        )

        object.__setattr__(
            self,
            "category",
            QuestionFieldParser.normalize_category(self.category),
        )

        QuestionValidator.validate(self)
