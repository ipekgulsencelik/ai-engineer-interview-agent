from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.report_template_schema import (
    REPORT_TEMPLATE_SCHEMA,
)


class ReportTemplateValidator:
    """
    ReportTemplate validation service.
    """

    SUPPORTED_TEMPLATE_FORMATS = frozenset(
        {
            "markdown",
            "html",
            "json",
            "pdf",
            "txt",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        template_id: str,
        name: str,
        report_type: str,
        template_format: str,
        template_content: str,
        version: str,
        created_at: datetime,
        created_by: str,
        title: str | None,
        description: str | None,
        enabled: bool,
        tags: tuple[
            str,
            ...,
        ],
        variables: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "template_id": template_id,
                "name": name,
                "report_type": report_type,
                "template_format": template_format,
                "template_content": template_content,
                "version": version,
                "created_at": created_at,
                "created_by": created_by,
                "title": title,
                "description": description,
                "enabled": enabled,
                "tags": tags,
                "variables": variables,
                "metadata": metadata or {},
            },
            schema=REPORT_TEMPLATE_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            template_format
            not in cls.SUPPORTED_TEMPLATE_FORMATS
        ):
            raise EvaluationValidationError(
                "template_format must be one of: "
                "markdown, html, json, pdf, txt."
            )

        cls._validate_tuple_values(
            values=tags,
            field_name="tags",
        )

        cls._validate_tuple_values(
            values=variables,
            field_name="variables",
        )

        if len(set(variables)) != len(variables):
            raise EvaluationValidationError(
                "variables must be unique."
            )

        if metadata is not None:
            for key, value in metadata.items():
                if (
                    not isinstance(
                        key,
                        str,
                    )
                    or not key.strip()
                ):
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )

    @staticmethod
    def _validate_tuple_values(
        *,
        values: tuple[
            str,
            ...,
        ],
        field_name: str,
    ) -> None:
        for index, value in enumerate(
            values,
        ):
            if (
                not isinstance(
                    value,
                    str,
                )
                or not value.strip()
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be a non-empty string."
                )