"""Pure release approval policy: fail closed, no cloud credentials or I/O.

This evaluates *operator-supplied evidence*, not its authenticity.
GitHub protected environments and independently signed attestations must
enforce the actual authorization boundary before production deployment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

_VERSION = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
_GIT_SHA = re.compile(r"[0-9a-f]{40}")
_IMAGE = re.compile(
    r"ghcr\.io/ipekgulsencelik/ai-engineer-interview-agent@"
    r"sha256:[0-9a-f]{64}"
)

_REQUIRED_APPROVALS = (
    "security_reviewed",
    "operations_approved",
    "database_migration_reviewed",
)
_REQUIRED_EVIDENCE = (
    "ci_green",
    "dependency_audit_passed",
    "container_scan_passed",
    "sbom_recorded",
    "backup_restore_tested",
    "rollback_drill_verified",
)


@dataclass(frozen=True, slots=True)
class ReleaseDecision:
    allowed: bool
    failed_checks: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "failed_checks": list(self.failed_checks),
            "assurance": (
                "Self-reported preflight only; production requires "
                "independent protected-environment verification"
            ),
        }


class ReleaseReadinessEvaluator:
    """Require digest-pinned deployment and explicit recorded approvals."""

    def evaluate(self, plan: Mapping[str, object]) -> ReleaseDecision:
        if not isinstance(plan, Mapping):
            raise ValueError("release plan must be an object")

        failed: list[str] = []
        version = plan.get("version")
        if not isinstance(version, str) or _VERSION.fullmatch(version) is None:
            failed.append("semantic_version")

        sha = plan.get("source_sha")
        if not isinstance(sha, str) or _GIT_SHA.fullmatch(sha) is None:
            failed.append("source_git_sha")

        image = plan.get("image")
        rollback_image = plan.get("rollback_image")
        if not isinstance(image, str) or _IMAGE.fullmatch(image) is None:
            failed.append("immutable_image_digest")
        if (
            not isinstance(rollback_image, str)
            or _IMAGE.fullmatch(rollback_image) is None
            or rollback_image == image
        ):
            failed.append("distinct_rollback_image_digest")

        for label, required in (
            ("approvals", _REQUIRED_APPROVALS),
            ("evidence", _REQUIRED_EVIDENCE),
        ):
            obj = plan.get(label)
            for field in required:
                if not isinstance(obj, Mapping) or obj.get(field) is not True:
                    failed.append(f"{label}.{field}")

        # No user-supplied arbitrary metadata is emitted in the decision.
        return ReleaseDecision(allowed=not failed, failed_checks=tuple(failed))
