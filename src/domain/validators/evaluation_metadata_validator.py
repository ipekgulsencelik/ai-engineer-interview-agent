from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)
from src.domain.validation.evaluation_metadata_validation_schema import (
    EVALUATION_METADATA_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.metadata.evaluation_metadata import (
        EvaluationMetadata,
    )


class EvaluationMetadataValidator(
    BaseSchemaValidator,
):
    """
    EvaluationMetadata invariant validation helper.
    """

    @classmethod
    def validate(
        cls,
        metadata: "EvaluationMetadata",
    ) -> None:
        from src.domain.metadata.evaluation_metadata import (
            EvaluationMetadata,
        )

        cls.validate_model_type(
            value=metadata,
            expected_type=EvaluationMetadata,
            field_name="metadata",
        )

        for model_field in fields(metadata):
            field_name = model_field.name

            value = getattr(
                metadata,
                field_name,
            )

            rules = (
                EVALUATION_METADATA_VALIDATION_SCHEMA[
                    field_name
                ]
            )

            cls.validate_nullable(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            if value is None:
                continue

            cls.validate_type(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls.validate_non_empty_string(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls.validate_numeric_bounds(
                field_name=field_name,
                value=value,
                rules=rules,
            )

            cls.validate_tuple_items(
                field_name=field_name,
                value=value,
                rules=rules,
            )