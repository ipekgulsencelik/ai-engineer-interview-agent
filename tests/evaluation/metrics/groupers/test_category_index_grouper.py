from __future__ import annotations

from src.evaluation.metrics.groupers.category_index_grouper import (
    CategoryIndexGrouper,
)


def test_category_index_grouper_should_group_indices_by_trimmed_category() -> None:
    grouped_indices = CategoryIndexGrouper.group(
        categories=(
            " RAG ",
            "MLOps",
            "RAG",
            "Agents",
            "MLOps ",
        ),
    )

    assert grouped_indices == {
        "RAG": (0, 2),
        "MLOps": (1, 4),
        "Agents": (3,),
    }
