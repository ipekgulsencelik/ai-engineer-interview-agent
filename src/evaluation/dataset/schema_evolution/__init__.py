"""Versioned record schemas and explicit migration contracts."""

from src.evaluation.dataset.schema_evolution.compatibility import (
    CompatibilityReport,
    SchemaCompatibilityChecker,
)
from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.migrations import (
    DropField,
    MigrationOperation,
    MigrationPathResolver,
    MigrationRegistry,
    MigrationStep,
    RecordMigration,
    RenameField,
    SetDefault,
)
from src.evaluation.dataset.schema_evolution.coordinator import (
    DatasetMigrationCoordinator,
    RecordMigrationPort,
)
from src.evaluation.dataset.schema_evolution.persistence import (
    MigrationAuditEvent,
    MigrationPersistencePort,
    MigrationSnapshot,
    MigrationTelemetryPort,
)
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
)
from src.evaluation.dataset.schema_evolution.service import (
    RecordValidationPort,
    SchemaCompatibilityPort,
    SchemaLookupPort,
    SchemaEvolutionService,
)
from src.evaluation.dataset.schema_evolution.validation import (
    DatasetRecordValidator,
)

__all__ = [
    "CompatibilityReport",
    "DatasetField",
    "DatasetMigrationCoordinator",
    "DatasetRecordSchema",
    "DatasetRecordValidator",
    "DropField",
    "MigrationAuditEvent",
    "MigrationOperation",
    "MigrationPersistencePort",
    "MigrationSnapshot",
    "MigrationTelemetryPort",
    "MigrationPathResolver",
    "MigrationRegistry",
    "MigrationStep",
    "RecordMigration",
    "RecordValidationPort",
    "RecordMigrationPort",
    "RenameField",
    "SchemaCompatibilityChecker",
    "SchemaCompatibilityPort",
    "SchemaLookupPort",
    "SchemaEvolutionError",
    "SchemaEvolutionService",
    "SetDefault",
]
