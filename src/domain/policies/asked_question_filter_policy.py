from __future__ import annotations

from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)


class AskedQuestionFilterPolicy:
    """
    Asked question exclusion policy.
    """

    @staticmethod
    def filter(
        *,
        search_results: list[QuestionSearchResult],
        asked_question_ids: tuple[str, ...],
    ) -> list[QuestionSearchResult]:
        asked_question_id_set = set(
            asked_question_ids,
        )

        return [
            result
            for result in search_results
            if result.question.id
            not in asked_question_id_set
        ]