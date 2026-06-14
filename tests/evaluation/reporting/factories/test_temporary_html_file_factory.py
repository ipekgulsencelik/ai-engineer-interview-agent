from __future__ import annotations

from src.evaluation.reporting.factories.temporary_html_file_factory import TemporaryHTMLFileFactory


def test_create_writes_html_to_temporary_file() -> None:
    path = TemporaryHTMLFileFactory.create(html="<p>temporary</p>")

    try:
        assert path.suffix == ".html"
        assert path.read_text(encoding="utf-8") == "<p>temporary</p>"
    finally:
        path.unlink(missing_ok=True)
