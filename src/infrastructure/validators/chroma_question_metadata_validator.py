from __future__ import annotations

from src.domain.constants.chroma_question import (
    CURRENT_QUESTION_METADATA_VERSION,
    SUPPORTED_QUESTION_METADATA_VERSIONS,
)
from src.infrastructure.validations.chroma.chroma_question_metadata_schema import (
    CHROMA_QUESTION_METADATA_SCHEMA,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    QuestionMetadata,
)


class ChromaQuestionMetadataValidator:
    """Validates raw question metadata payloads returned by ChromaDB."""

    @staticmethod
    def validate(metadata: QuestionMetadata) -> None:
        missing = [
            field
            for field, rules in CHROMA_QUESTION_METADATA_SCHEMA.items()
            if rules.get("required") and field not in metadata
        ]
        if missing:
            raise ValueError(f"Missing required metadata fields: {', '.join(missing)}")

        for field, rules in CHROMA_QUESTION_METADATA_SCHEMA.items():
            if field not in metadata:
                continue

            expected_type = rules["type"]
            if not isinstance(metadata[field], expected_type):
                raise TypeError(
                    f"Invalid type for metadata field '{field}': "
                    f"expected {expected_type}, got {type(metadata[field])}"
                )

        version = metadata.get("metadata_version", CURRENT_QUESTION_METADATA_VERSION)
        if version not in SUPPORTED_QUESTION_METADATA_VERSIONS:
            raise ValueError(
                "Unsupported metadata_version: "
                f"{version}. Supported versions: {sorted(SUPPORTED_QUESTION_METADATA_VERSIONS)}"
            )