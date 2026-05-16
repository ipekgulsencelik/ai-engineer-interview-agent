from __future__ import annotations

from src.domain.resolvers.question_category_aliases import (
    QUESTION_CATEGORY_ALIASES,
)


class QuestionCategoryAliasResolver:
    """
    QuestionCategory alias resolution policy.
    """

    def resolve(
        self,
        *,
        value: str,
    ) -> str:
        return QUESTION_CATEGORY_ALIASES.get(
            value,
            value,
        )