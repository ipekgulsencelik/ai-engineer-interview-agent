from __future__ import annotations

from src.domain.scoring.scoring_context import (
    ScoringContext,
)
from src.domain.value_objects.search_filters import (
    SearchFilters,
)


class SearchFiltersBuilder:
    """
    Search filter construction helper.
    """

    @staticmethod
    def build(
        *,
        context: ScoringContext,
    ) -> SearchFilters:
        return SearchFilters(
            level=getattr(
                context,
                "current_level",
                None,
            ),
        )