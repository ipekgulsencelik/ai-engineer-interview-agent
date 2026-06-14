from __future__ import annotations

from html import escape


class HTMLRenderingUtils:
    """
    Shared HTML rendering helpers.
    """

    @staticmethod
    def document(
        *,
        title: str,
        body: str,
    ) -> str:
        escaped_title = escape(
            title,
        )

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escaped_title}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 40px;
      line-height: 1.6;
      color: #1f2937;
      background: #ffffff;
    }}
    h1 {{
      color: #111827;
      border-bottom: 2px solid #e5e7eb;
      padding-bottom: 12px;
    }}
    h2 {{
      margin-top: 32px;
      color: #374151;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin-top: 12px;
    }}
    th, td {{
      border: 1px solid #d1d5db;
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f3f4f6;
    }}
    ul {{
      margin-top: 8px;
    }}
    .empty {{
      color: #6b7280;
      font-style: italic;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""

    @staticmethod
    def h1(
        value: str,
    ) -> str:
        return f"<h1>{escape(value)}</h1>"

    @staticmethod
    def section(
        *,
        title: str,
        content: str,
    ) -> str:
        return "\n".join(
            [
                "<section>",
                f"<h2>{escape(title)}</h2>",
                content,
                "</section>",
            ]
        )

    @staticmethod
    def paragraph(
        value: str,
    ) -> str:
        return f"<p>{escape(value)}</p>"

    @staticmethod
    def list(
        *,
        values: tuple[
            str,
            ...,
        ],
    ) -> str:
        if not values:
            return '<p class="empty">None.</p>'

        items = "\n".join(
            f"<li>{escape(value)}</li>"
            for value in values
        )

        return (
            "<ul>\n"
            f"{items}\n"
            "</ul>"
        )

    @staticmethod
    def table(
        *,
        rows: dict[
            str,
            object,
        ],
    ) -> str:
        rendered_rows = "\n".join(
            "<tr>"
            f"<td>{escape(key)}</td>"
            f"<td>{escape(HTMLRenderingUtils.format_value(value))}</td>"
            "</tr>"
            for key, value in rows.items()
        )

        return (
            "<table>\n"
            "<thead>"
            "<tr><th>Metric</th><th>Value</th></tr>"
            "</thead>\n"
            "<tbody>\n"
            f"{rendered_rows}\n"
            "</tbody>\n"
            "</table>"
        )

    @staticmethod
    def format_value(
        value: object,
    ) -> str:
        if value is None:
            return "-"

        if isinstance(
            value,
            float,
        ):
            return f"{value:.4f}"

        return str(
            value,
        )