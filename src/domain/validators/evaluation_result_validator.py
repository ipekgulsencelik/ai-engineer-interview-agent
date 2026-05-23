from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)
from src.domain.validation.evaluation_result_validation_schema import (
    EVALUATION_RESULT_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.evaluation_result import (
        EvaluationResult,
    )


class EvaluationResultValidator(
    BaseSchemaValidator,
):
    """
    EvaluationResult invariant validation helper.
    """

    @classmethod
    def validate(
        cls,
        result: "EvaluationResult",
    ) -> None:
        from src.domain.results.evaluation_result import (
            EvaluationResult,
        )

        cls.validate_model_type(
            value=result,
            expected_type=EvaluationResult,
            field_name="result",
        )

        for model_field in fields(result):
            field_name = model_field.name

            value = getattr(
                result,
                field_name,
            )

            rules = (
                EVALUATION_RESULT_VALIDATION_SCHEMA[
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