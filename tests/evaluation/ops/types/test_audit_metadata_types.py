from __future__ import annotations

from src.evaluation.ops.types.audit_metadata import AuditMetadata, AuditMetadataValue


def test_audit_metadata_type_aliases_should_support_expected_runtime_payload_shape() -> (
    None
):
    value: AuditMetadataValue = "stage"
    metadata: AuditMetadata = {
        "stage": value,
        "attempt": 1,
        "score": 0.91,
        "passed": True,
    }

    assert metadata == {
        "stage": "stage",
        "attempt": 1,
        "score": 0.91,
        "passed": True,
    }
