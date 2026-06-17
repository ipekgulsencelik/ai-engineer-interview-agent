from __future__ import annotations

import re


class TemplateVariableExtractor:
    """
    Extracts variable placeholders from template content.
    """

    VARIABLE_PATTERN = re.compile(
        r"{{\s*([a-zA-Z_][a-zA-Z0-9_\.]*)\s*}}",
    )

    def extract(
        self,
        *,
        template_content: str,
    ) -> tuple[
        str,
        ...,
    ]:
        return tuple(
            dict.fromkeys(
                match.group(
                    1,
                )
                for match in self.VARIABLE_PATTERN.finditer(
                    template_content,
                )
            )
        )