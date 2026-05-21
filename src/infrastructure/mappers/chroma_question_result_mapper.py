from __future__ import annotations

from src.domain.entities.question import Question
from src.infrastructure.constants.vector_metadata_keys import (
    QUESTION_ID_METADATA_KEY,
)
from src.infrastructure.rehydrators.question_rehydrator import (
    QuestionRehydrator,
)
from src.infrastructure.validators.chroma_question_metadata_validator import (
    ChromaQuestionMetadataValidator,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaQuestionMetadata,
)


class ChromaQuestionResultMapper:
    """
    Chroma metadata -> Question entity mapper.
    """

    def __init__(
        self,
        *,
        question_rehydrator: QuestionRehydrator | None = None,
    ) -> None:
        self._question_rehydrator = (
            question_rehydrator
            or QuestionRehydrator()
        )

    def to_question(
        self,
        *,
        metadata: ChromaQuestionMetadata,
        fallback_question_id: str | None = None,
    ) -> Question:
        ChromaQuestionMetadataValidator.validate(
            metadata=metadata,
        )

        return self._question_rehydrator.rehydrate(
            question_id=self._resolve_question_id(
                metadata=metadata,
                fallback_question_id=fallback_question_id,
            ),
            metadata=dict(metadata),
        )

    @staticmethod
    def _resolve_question_id(
        *,
        metadata: ChromaQuestionMetadata,
        fallback_question_id: str | None,
    ) -> str:
        question_id = metadata.get(
            QUESTION_ID_METADATA_KEY,
            fallback_question_id,
        )

        if question_id is None:
            return ""

        return str(question_id)