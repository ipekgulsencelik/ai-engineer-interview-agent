from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from src.evaluation.reporting.resolvers.template_context_path_resolver import (
    TemplateContextPathResolver,
)
from src.evaluation.reporting.extractors.template_variable_extractor import (
    TemplateVariableExtractor,
)


class TemplateInterpolator:
    """
    Interpolates template variables using context values.
    """

    def __init__(
        self,
        *,
        path_resolver: TemplateContextPathResolver,
    ) -> None:
        self._path_resolver = path_resolver

    def interpolate(
        self,
        *,
        template_content: str,
        context: Mapping[
            str,
            Any,
        ],
    ) -> str:
        return TemplateVariableExtractor.VARIABLE_PATTERN.sub(
            lambda match: self._resolve_match(
                match=match,
                context=context,
            ),
            template_content,
        )

    def _resolve_match(
        self,
        *,
        match: re.Match[
            str,
        ],
        context: Mapping[
            str,
            Any,
        ],
    ) -> str:
        variable_path = match.group(
            1,
        )

        value = self._path_resolver.resolve(
            context=context,
            path=variable_path,
        )

        if value is None:
            return ""

        return str(
            value,
        )