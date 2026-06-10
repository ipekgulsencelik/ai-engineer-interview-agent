from __future__ import annotations

from enum import StrEnum
from typing import Generic, TypeVar

from src.domain.errors.factories.enum_parsing_error_factory import (
    EnumParsingErrorFactory,
)
from src.domain.normalizers.contracts.enum_value_normalizer import (
    EnumValueNormalizer,
)
from src.domain.resolvers.contracts.enum_value_resolver import (
    EnumValueResolver,
)
from src.domain.resolvers.implementations.identity_enum_value_resolver import (
    IdentityEnumValueResolver,
)
from src.domain.validators.enum_parser_configuration_validator import (
    EnumParserConfigurationValidator,
)
from src.domain.validators.enum_parser_validator import (
    EnumParserValidator,
)

EnumT = TypeVar(
    "EnumT",
    bound=StrEnum,
)


class DefaultEnumParser(Generic[EnumT]):
    """
    Generic enum parser orchestration.
    """

    def __init__(
        self,
        *,
        enum_class: type[EnumT],
        field_name: str,
        normalizer: EnumValueNormalizer,
        resolver: EnumValueResolver | None = None,
    ) -> None:
        EnumParserConfigurationValidator.validate_field_name(
            field_name=field_name,
        )

        self._enum_class = enum_class
        self._field_name = field_name
        self._normalizer = normalizer
        self._resolver = resolver or IdentityEnumValueResolver()

    def parse(
        self,
        value: EnumT | str,
    ) -> EnumT:
        EnumParserValidator.validate_raw_enum_input(
            value=value,
            enum_class=self._enum_class,
            field_name=self._field_name,
        )

        if isinstance(value, self._enum_class):
            return value

        normalized_value = self._normalizer.normalize(
            value=value,
        )

        resolved_value = self._resolver.resolve(
            value=normalized_value,
        )

        try:
            return self._enum_class(
                resolved_value,
            )

        except ValueError as exc:
            raise EnumParsingErrorFactory.invalid_enum(
                field_name=self._field_name,
                value=value,
                enum_class=self._enum_class,
            ) from exc