from __future__ import annotations

from src.infrastructure.models.search_result import (
    SearchResult,
)


class CategoryHitPolicy:
    """
    Category hit calculation policy.
    """

    @staticmethod
    def has_hit(
        *,
        expected_category: str,
        search_results: list[SearchResult],
    ) -> bool:
        return any(
            result.question.category.value
            == expected_category
            for result in search_results
        )