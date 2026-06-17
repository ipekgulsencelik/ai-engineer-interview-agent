from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.validators.report_template_validator import (
    ReportTemplateValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReportTemplate:
    """
    Immutable report template.

    Defines reusable report rendering templates
    for executive summaries, benchmark reports,
    trend reports, comparison reports, dashboards,
    scheduled reports, and analytics exports.
    """

    template_id: str

    name: str

    report_type: str

    template_format: str

    template_content: str

    version: str

    created_at: datetime

    created_by: str

    title: str | None = None

    description: str | None = None

    enabled: bool = True

    tags: tuple[
        str,
        ...,
    ] = ()

    variables: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ReportTemplateValidator.validate(
            template_id=self.template_id,
            name=self.name,
            report_type=self.report_type,
            template_format=self.template_format,
            template_content=self.template_content,
            version=self.version,
            created_at=self.created_at,
            created_by=self.created_by,
            title=self.title,
            description=self.description,
            enabled=self.enabled,
            tags=self.tags,
            variables=self.variables,
            metadata=self.metadata,
        )

    @property
    def display_name(
        self,
    ) -> str:
        return (
            self.title
            or self.name
        )

    @property
    def has_title(
        self,
    ) -> bool:
        return (
            self.title
            is not None
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_tags(
        self,
    ) -> bool:
        return bool(
            self.tags,
        )

    @property
    def has_variables(
        self,
    ) -> bool:
        return bool(
            self.variables,
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def variable_count(
        self,
    ) -> int:
        return len(
            self.variables,
        )

    @property
    def tag_count(
        self,
    ) -> int:
        return len(
            self.tags,
        )

    @property
    def is_markdown(
        self,
    ) -> bool:
        return (
            self.template_format
            == "markdown"
        )

    @property
    def is_html(
        self,
    ) -> bool:
        return (
            self.template_format
            == "html"
        )

    @property
    def is_pdf(
        self,
    ) -> bool:
        return (
            self.template_format
            == "pdf"
        )

    @property
    def is_json(
        self,
    ) -> bool:
        return (
            self.template_format
            == "json"
        )