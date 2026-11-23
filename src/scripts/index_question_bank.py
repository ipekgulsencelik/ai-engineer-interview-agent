"""Index the question bank into the local Chroma collection.

Usage:
    uv run python -m src.scripts.index_question_bank
    uv run python -m src.scripts.index_question_bank --bank data/question_bank/questions.json

Re-running is safe: questions are upserted by id. Questions removed from the
bank are deleted from the collection so the index always mirrors the file.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from src.application.ports.embedding_provider import EmbeddingProvider
from src.application.services.question_indexing_service import (
    QuestionIndexingService,
)
from src.application.use_cases.load_questions_use_case import (
    LoadQuestionsUseCase,
)
from src.domain.entities.question import Question
from src.infrastructure.constants.chroma_defaults import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
)
from src.infrastructure.embedding.sentence_transformer_embedding_provider_factory import (
    DEFAULT_EMBEDDING_MODEL_NAME,
    SentenceTransformerEmbeddingProviderFactory,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)
from src.infrastructure.vector_stores.chroma.chroma_client_factory import (
    create_chroma_client,
)
from src.infrastructure.vector_stores.chroma.chroma_collection_factory import (
    get_or_create_chroma_collection,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)

DEFAULT_BANK_PATH = Path("data/question_bank/questions.json")


def index_question_bank(
    *,
    bank_path: Path,
    persist_directory: str,
    collection_name: str,
    embedding_provider: EmbeddingProvider,
) -> list[Question]:
    """Load, embed and upsert all questions; prune ids no longer in the bank."""
    repository = JsonQuestionRepositoryBuilder.build_default(file_path=bank_path)
    questions = LoadQuestionsUseCase(question_repository=repository).execute()

    collection = get_or_create_chroma_collection(
        client=create_chroma_client(persist_directory=persist_directory),
        collection_name=collection_name,
    )

    QuestionIndexingService(
        embedding_provider=embedding_provider,
        vector_store=ChromaQuestionVectorStore(collection=collection),
    ).index_questions(questions=questions)

    current_ids = {question.id for question in questions}
    stale_ids = [qid for qid in collection.get()["ids"] if qid not in current_ids]
    if stale_ids:
        collection.delete(ids=stale_ids)

    return questions


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    parser.add_argument("--persist-dir", default=DEFAULT_CHROMA_PERSIST_DIRECTORY)
    parser.add_argument("--collection", default=DEFAULT_CHROMA_COLLECTION_NAME)
    parser.add_argument("--model", default=DEFAULT_EMBEDDING_MODEL_NAME)
    args = parser.parse_args(argv)

    questions = index_question_bank(
        bank_path=args.bank,
        persist_directory=args.persist_dir,
        collection_name=args.collection,
        embedding_provider=SentenceTransformerEmbeddingProviderFactory.build(
            model_name=args.model,
        ),
    )
    print(
        f"Indexed {len(questions)} questions into "
        f"'{args.collection}' at {args.persist_dir}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
