from __future__ import annotations


class MarkdownListFormatter:
    """
    Markdown bullet list formatter.
    """

    @staticmethod
    def format(
        *,
        items: tuple[str, ...],
    ) -> str:
        return "\n".join(
            f"- {item}"
            for item in items
        )