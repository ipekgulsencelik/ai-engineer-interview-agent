from __future__ import annotations


class ValidationFormatter:
    """
    Validation formatting utilities.
    """

    @staticmethod
    def format_type_name(
        expected_type: type | tuple[type, ...],
    ) -> str:
        """
        Convert a runtime type definition into a human-readable string.

        Examples:
            str -> "str"
            (int, float) -> "int or float"
        """

        if isinstance(
            expected_type,
            tuple,
        ):
            return " or ".join(
                item.__name__
                for item in expected_type
            )

        return expected_type.__name__