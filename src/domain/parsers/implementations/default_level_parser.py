from __future__ import annotations

from src.domain.enums.level import Level
from src.domain.normalizers.implementations.uppercase_enum_value_normalizer import (
    UppercaseEnumValueNormalizer,
)
from src.domain.parsers.implementations.default_enum_parser import (
    DefaultEnumParser,
)


class DefaultLevelParser(DefaultEnumParser[Level]):
    """
    Default Level parser.
    """

    def __init__(self) -> None:
        super().__init__(
            enum_class=Level,
            field_name="level",
            normalizer=UppercaseEnumValueNormalizer(),
        )