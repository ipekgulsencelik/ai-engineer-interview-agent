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
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
)
from src.evaluation.dataset.schema_evolution.service import (
    RecordValidationPort,
    SchemaCompatibilityPort,
    SchemaEvolutionService,
)
from src.evaluation.dataset.schema_evolution.validation import (
    DatasetRecordValidator,
)

__all__ = [
    "CompatibilityReport",
    "DatasetField",
    "DatasetRecordSchema",
    "DatasetRecordValidator",
    "DropField",
    "MigrationOperation",
    "MigrationPathResolver",
    "MigrationRegistry",
    "MigrationStep",
    "RecordMigration",
    "RecordValidationPort",
    "RenameField",
    "SchemaCompatibilityChecker",
    "SchemaCompatibilityPort",
    "SchemaEvolutionError",
    "SchemaEvolutionService",
    "SetDefault",
]
