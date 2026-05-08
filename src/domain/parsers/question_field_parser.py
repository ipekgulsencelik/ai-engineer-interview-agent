from src.domain.enums.level import Level
from src.domain.enums.question_type import QuestionType


class QuestionFieldParser:
    @staticmethod
    def parse_level(level: Level | str) -> Level:
        if isinstance(level, Level):
            return level

        level_value = str(level).strip().upper()
        try:
            return Level(level_value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid question level: {level}. "
                f"Expected one of: {[level_item.value for level_item in Level]}"
            ) from exc

    @staticmethod
    def parse_question_type(question_type: QuestionType | str) -> QuestionType:
        if isinstance(question_type, QuestionType):
            return question_type

        question_type_value = str(question_type).strip().lower()
        try:
            return QuestionType(question_type_value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid question type: {question_type}. "
                f"Expected one of: "
                f"{[question_type_item.value for question_type_item in QuestionType]}"
            ) from exc

    @staticmethod
    def normalize_category(category: str) -> str:
        return str(category).strip()
