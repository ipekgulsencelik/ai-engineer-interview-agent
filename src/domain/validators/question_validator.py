from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.question.question import Question


class QuestionValidator:
    @staticmethod
    def validate(question: "Question") -> None:
        if not question.id.strip():
            raise ValueError("Question id cannot be empty.")

        if not question.text.strip():
            raise ValueError("Question text cannot be empty.")

        if not question.category.strip():
            raise ValueError("Question category cannot be empty.")

        if question.difficulty < 1 or question.difficulty > 3:
            raise ValueError("Question difficulty must be between 1 and 3.")

        if question.market_weight < 0 or question.market_weight > 1:
            raise ValueError("Market weight must be between 0 and 1.")

        if not isinstance(question.expected_points, list) or not all(
            isinstance(point, str) for point in question.expected_points
        ):
            raise ValueError("expected_points must be list[str].")

        if not isinstance(question.keywords, list) or not all(
            isinstance(keyword, str) for keyword in question.keywords
        ):
            raise ValueError("keywords must be list[str].")
