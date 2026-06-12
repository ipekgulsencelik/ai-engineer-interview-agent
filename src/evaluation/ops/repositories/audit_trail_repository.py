from __future__ import annotations

from abc import ABC, abstractmethod

from src.evaluation.ops.entities.evaluation_audit_trail import (
    EvaluationAuditTrail,
)


class AuditTrailRepository(
    ABC,
):
    """
    Audit trail repository contract.
    """

    @abstractmethod
    def save(
        self,
        *,
        trail: EvaluationAuditTrail,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_run_id(
        self,
        *,
        evaluation_run_id: str,
    ) -> (
        EvaluationAuditTrail
        | None
    ):
        raise NotImplementedError