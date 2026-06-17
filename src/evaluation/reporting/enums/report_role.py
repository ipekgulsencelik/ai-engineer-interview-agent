from __future__ import annotations

from enum import StrEnum


class ReportRole(
    StrEnum,
):
    """
    Report access role.
    """

    OWNER = "owner"

    ADMIN = "admin"

    ANALYST = "analyst"

    EDITOR = "editor"

    VIEWER = "viewer"

    AUDITOR = "auditor"