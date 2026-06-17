from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.entities.report_template import (
    ReportTemplate,
)
from src.evaluation.reporting.resolvers.template_context_path_resolver import (
    TemplateContextPathResolver,
)
from src.evaluation.reporting.extractors.template_variable_extractor import (
    TemplateVariableExtractor,
)


class TemplateVariableValidator:
    """
    Validates template state and declared variables.
    """

    def __init__(
        self,
        *,
        variable_extractor: TemplateVariableExtractor,
        path_resolver: TemplateContextPathResolver,
    ) -> None:
        self._variable_extractor = variable_extractor
        self._path_resolver = path_resolver

    def validate_enabled(
        self,
        *,
        template: ReportTemplate,
    ) -> None:
        if not template.enabled:
            raise EvaluationValidationError(
                "report template is disabled.",
            )

    def validate_required_variables(
        self,
        *,
        template: ReportTemplate,
        context: Mapping[
            str,
            Any,
        ],
    ) -> None:
        for variable in template.variables:
            if not self._path_resolver.has_path(
                context=context,
                path=variable,
            ):
                raise EvaluationValidationError(
                    "missing template variable: "
                    f"{variable}",
                )

    def validate_declared_variables(
        self,
        *,
        template: ReportTemplate,
    ) -> None:
        extracted_variables = set(
            self._variable_extractor.extract(
                template_content=template.template_content,
            )
        )

        declared_variables = set(
            template.variables,
        )

        missing_declarations = (
            extracted_variables
            - declared_variables
        )

        if missing_declarations:
            raise EvaluationValidationError(
                "template contains undeclared variables: "
                + ", ".join(
                    sorted(
                        missing_declarations,
                    )
                ),
            )