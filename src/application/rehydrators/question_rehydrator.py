from __future__ import annotations

from typing import Any

from src.domain.entities.question import Question
from src.domain.parsers.factories.question_field_parser_factory import (
    QuestionFieldParserFactory,
)
from src.domain.parsers.question_field_parser import (
    QuestionFieldParser,
)
from src.infrastructure.constants.question_rehydration_defaults import (
    DEFAULT_REHYDRATED_FOLLOWUP_ALLOWED,
    DEFAULT_REHYDRATED_MARKET_WEIGHT,
)
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    EXPECTED_POINTS_METADATA_KEY,
    FOLLOWUP_ALLOWED_METADATA_KEY,
    FOLLOWUP_METADATA_KEY,
    IDEAL_ANSWER_HINT_METADATA_KEY,
    KEYWORDS_METADATA_KEY,
    LEVEL_METADATA_KEY,
    MARKET_WEIGHT_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
    TEXT_METADATA_KEY,
)
from src.infrastructure.validators.question_metadata_rehydration_validator import (
    QuestionMetadataRehydrationValidator,
)


class QuestionRehydrator:
    """
    Persisted metadata -> Question entity reconstruction.
    """

    def __init__(
        self,
        *,
        field_parser: QuestionFieldParser | None = None,
    ) -> None:
        self._field_parser = (
            field_parser
            or QuestionFieldParserFactory.create_default()
        )

    def rehydrate(
        self,
        *,
        question_id: str,
        metadata: dict[str, Any],
    ) -> Question:
        QuestionMetadataRehydrationValidator.validate(
            question_id=question_id,
            metadata=metadata,
        )

        return Question(
            id=question_id.strip(),
            text=str(metadata[TEXT_METADATA_KEY]).strip(),
            category=self._field_parser.parse_category(
                metadata[CATEGORY_METADATA_KEY],
            ),
            level=self._field_parser.parse_level(
                metadata[LEVEL_METADATA_KEY],
            ),
            difficulty=int(
                metadata[DIFFICULTY_METADATA_KEY],
            ),
            question_type=self._field_parser.parse_question_type(
                metadata[QUESTION_TYPE_METADATA_KEY],
            ),
            expected_points=list(
                metadata.get(
                    EXPECTED_POINTS_METADATA_KEY,
                    [],
                )
            ),
            keywords=list(
                metadata.get(
                    KEYWORDS_METADATA_KEY,
                    [],
                )
            ),
            followup=metadata.get(
                FOLLOWUP_METADATA_KEY,
            ),
            ideal_answer_hint=metadata.get(
                IDEAL_ANSWER_HINT_METADATA_KEY,
            ),
            market_weight=float(
                metadata.get(
                    MARKET_WEIGHT_METADATA_KEY,
                    DEFAULT_REHYDRATED_MARKET_WEIGHT,
                )
            ),
            followup_allowed=bool(
                metadata.get(
                    FOLLOWUP_ALLOWED_METADATA_KEY,
                    DEFAULT_REHYDRATED_FOLLOWUP_ALLOWED,
                )
            ),
        )