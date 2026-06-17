from __future__ import annotations


class BrandInlineCSSBuilder:
    """
    Builds inline CSS from CSS variable mappings.
    """

    def build(
        self,
        *,
        variables: dict[
            str,
            str,
        ],
    ) -> str:
        return (
            ":root {\n"
            + "\n".join(
                f"  {key}: {value};"
                for key, value in variables.items()
            )
            + "\n}"
        )