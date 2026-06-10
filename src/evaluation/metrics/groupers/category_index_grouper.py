from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence


class CategoryIndexGrouper:
    """
    Groups sample indices by normalized category name.
    """

    @staticmethod
    def group(
        *,
        categories: Sequence[str],
    ) -> dict[str, tuple[int, ...]]:
        grouped_indices: dict[str, list[int]] = defaultdict(list)

        for index, category in enumerate(categories):
            normalized_category = category.strip()

            grouped_indices[normalized_category].append(index)

        return {
            category: tuple(indices)
            for category, indices in grouped_indices.items()
        }