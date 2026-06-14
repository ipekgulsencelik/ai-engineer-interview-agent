from __future__ import annotations


class MarkdownRenderingUtils:
    """
    Shared Markdown rendering helpers.
    """

    @staticmethod
    def render_kpi_table(
        *,
        rows: dict[
            str,
            object,
        ],
    ) -> str:
        lines = [
            "| Metric | Value |",
            "| ------ | ----- |",
        ]

        for key, value in rows.items():
            lines.append(
                f"| {key} | "
                f"{MarkdownRenderingUtils.format_value(value)} |"
            )

        return "\n".join(
            lines,
        )

    @staticmethod
    def render_list_section(
        *,
        title: str,
        values: tuple[
            str,
            ...,
        ],
    ) -> str:
        lines = [
            f"## {title}",
        ]

        if not values:
            lines.append(
                "_None._",
            )

            return "\n".join(
                lines,
            )

        lines.extend(
            f"- {value}"
            for value in values
        )

        return "\n".join(
            lines,
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