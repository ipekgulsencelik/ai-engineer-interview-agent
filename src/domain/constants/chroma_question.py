from __future__ import annotations

REQUIRED_QUESTION_METADATA_FIELDS = (
    "id",
    "text",
    "category",
    "level",
    "difficulty",
    "question_type",
)

CURRENT_QUESTION_METADATA_VERSION = "v1"
SUPPORTED_QUESTION_METADATA_VERSIONS = {
    CURRENT_QUESTION_METADATA_VERSION,
}