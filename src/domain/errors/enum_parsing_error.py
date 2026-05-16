from __future__ import annotations

from src.domain.errors.parsing_error import ParsingError


class EnumParsingError(ParsingError):
    """
    Raised when enum parsing fails.
    """