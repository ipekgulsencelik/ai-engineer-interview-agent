from __future__ import annotations

from src.evaluation.reporting.utils.html_rendering_utils import HTMLRenderingUtils


def test_html_utils_escape_user_controlled_values() -> None:
    assert HTMLRenderingUtils.h1("<script>") == "<h1>&lt;script&gt;</h1>"
    assert "&lt;tag&gt;" in HTMLRenderingUtils.paragraph("<tag>")
    assert '<p class="empty">None.</p>' == HTMLRenderingUtils.list(values=())
    assert "0.1235" in HTMLRenderingUtils.table(rows={"Score": 0.12345})
