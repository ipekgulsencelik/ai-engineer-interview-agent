from __future__ import annotations

from pathlib import Path

from src.infrastructure.loaders.question_bank_loader import (
    QuestionBankLoader,
)
from src.infrastructure.mappers.question_mapper import (
    QuestionMapper,
)
from src.infrastructure.path_resolvers.question_bank_path_resolver import (
    QuestionBankPathResolver,
)
from src.infrastructure.readers.json_file_reader import (
    JsonFileReader,
)
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.validators.question_bank_path_validator import (
    QuestionBankPathValidator,
)
from src.infrastructure.validators.question_repository_config_validator import (
    QuestionRepositoryConfigValidator,
)


class JsonQuestionRepositoryBuilder:
    """
    JsonQuestionRepository dependency composition builder.
    """

    @staticmethod
    def build_default(
        *,
        file_path: str | Path,
    ) -> JsonQuestionRepository:
        QuestionRepositoryConfigValidator.validate_file_path(
            file_path,
        )

        resolved_path = Path(file_path)

        QuestionBankPathValidator.validate_file_path(
            file_path=resolved_path,
        )

        return JsonQuestionRepository(
            loader=QuestionBankLoader(
                file_path=resolved_path,
                path_resolver=QuestionBankPathResolver(),
                json_reader=JsonFileReader(),
            ),
            mapper=QuestionMapper(),
        )