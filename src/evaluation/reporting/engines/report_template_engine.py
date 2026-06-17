from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.evaluation.reporting.entities.report_template import (
    ReportTemplate,
)
from src.evaluation.reporting.services.template_interpolator import (
    TemplateInterpolator,
)
from src.evaluation.reporting.extractors.template_variable_extractor import (
    TemplateVariableExtractor,
)
from src.evaluation.reporting.validators.template_variable_validator import (
    TemplateVariableValidator,
)


class ReportTemplateEngine:
    """
    Facade template rendering engine for report templates.
    """

    def __init__(
        self,
        *,
        variable_extractor: TemplateVariableExtractor,
        variable_validator: TemplateVariableValidator,
        interpolator: TemplateInterpolator,
    ) -> None:
        self._variable_extractor = variable_extractor
        self._variable_validator = variable_validator
        self._interpolator = interpolator

    def render(
        self,
        *,
        template: ReportTemplate,
        context: Mapping[
            str,
            Any,
        ],
    ) -> str:
        self._variable_validator.validate_enabled(
            template=template,
        )

        self._variable_validator.validate_required_variables(
            template=template,
            context=context,
        )

        return self._interpolator.interpolate(
            template_content=template.template_content,
            context=context,
        )

    def extract_variables(
        self,
        *,
        template_content: str,
    ) -> tuple[
        str,
        ...,
    ]:
        return self._variable_extractor.extract(
            template_content=template_content,
        )

    def validate_template_variables(
        self,
        *,
        template: ReportTemplate,
    ) -> None:
        self._variable_validator.validate_declared_variables(
            template=template,
        )