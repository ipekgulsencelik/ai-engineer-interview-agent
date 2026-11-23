"""One-time trusted JSON -> SQLite question-vector indexing entrypoint.

Do not import or deserialize Chroma persistence. For a rebuild, select a fresh
index path, validate the source records and re-embed using a reviewed model.
"""

from __future__ import annotations

from pathlib import Path

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.ports.question_repository import QuestionRepository
from src.application.ports.question_vector_store import QuestionVectorStore
from src.application.services.question_indexing_service import QuestionIndexingService
from src.application.use_cases.load_questions_use_case import LoadQuestionsUseCase
from src.config.settings import settings
from src.infrastructure.containers.retrieval_container import RetrievalContainer
from src.infrastructure.loaders.question_bank_loader import QuestionBankLoader
from src.infrastructure.mappers.question_mapper import QuestionMapper
from src.infrastructure.path_resolvers.question_bank_path_resolver import (
    QuestionBankPathResolver,
)
from src.infrastructure.readers.json_file_reader import JsonFileReader
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.vector_stores.sqlite.sqlite_question_vector_store import (
    SqliteQuestionVectorStore,
)


def index_from_repository(
    *,
    repository: QuestionRepository,
    embedding_provider: EmbeddingProvider,
    vector_store: QuestionVectorStore,
) -> int:
    """Orchestrate a validated index build with injectable application ports."""
    questions = LoadQuestionsUseCase(
        question_repository=repository,
    ).execute()
    if not questions:
        raise ValueError("Trusted question bank is empty; refusing to index.")
    QuestionIndexingService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    ).index_questions(questions=questions)
    return len(questions)


def main() -> None:
    repository = JsonQuestionRepository(
        loader=QuestionBankLoader(
            file_path=Path(settings.QUESTION_DATA_PATH),
            path_resolver=QuestionBankPathResolver(),
            json_reader=JsonFileReader(),
        ),
        mapper=QuestionMapper(),
    )
    container = RetrievalContainer()
    store = container.vector_store
    if not isinstance(store, SqliteQuestionVectorStore):
        raise RuntimeError("Only trusted SQLite reindex is supported.")
    if store.count() != 0:
        raise RuntimeError(
            "Refusing to reindex a nonempty database; select a fresh "
            "QUESTION_VECTOR_DB_PATH after backup."
        )
    indexed = index_from_repository(
        repository=repository,
        embedding_provider=container.embedding_provider,
        vector_store=store,
    )
    print(f"Indexed {indexed} trusted questions into SQLite.")


if __name__ == "__main__":
    main()
