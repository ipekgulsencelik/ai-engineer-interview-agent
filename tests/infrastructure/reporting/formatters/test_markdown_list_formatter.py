from __future__ import annotations

from src.infrastructure.reporting.formatters.markdown_list_formatter import MarkdownListFormatter


def test_format_returns_markdown_bullets() -> None:
    assert MarkdownListFormatter.format(items=("one", "two")) == "- one\n- two"


def test_format_returns_empty_string_for_empty_items() -> None:
    assert MarkdownListFormatter.format(items=()) == ""
