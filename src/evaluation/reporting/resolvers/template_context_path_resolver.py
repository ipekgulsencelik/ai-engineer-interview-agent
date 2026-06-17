from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class TemplateContextPathResolver:
    """
    Resolves dot-notation variable paths from template context.
    """

    def resolve(
        self,
        *,
        context: Mapping[
            str,
            Any,
        ],
        path: str,
    ) -> Any:
        current: Any = context

        for part in path.split(
            ".",
        ):
            if isinstance(
                current,
                Mapping,
            ):
                if part not in current:
                    raise KeyError(
                        part,
                    )

                current = current[
                    part
                ]
                continue

            if not hasattr(
                current,
                part,
            ):
                raise KeyError(
                    part,
                )

            current = getattr(
                current,
                part,
            )

        return current

    def has_path(
        self,
        *,
        context: Mapping[
            str,
            Any,
        ],
        path: str,
    ) -> bool:
        try:
            self.resolve(
                context=context,
                path=path,
            )
        except KeyError:
            return False

        return True