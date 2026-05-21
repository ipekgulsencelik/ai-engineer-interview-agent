from __future__ import annotations

from pathlib import Path

from src.application.services.question_indexing_service import (
    QuestionIndexingService,
)
from src.application.use_cases.load_questions_use_case import (
    LoadQuestionsUseCase,
)
from src.infrastructure.builders.chroma_question_vector_store_builder import (
    ChromaQuestionVectorStoreBuilder,
)
from src.infrastructure.builders.sentence_transformer_embedding_provider_builder import (
    SentenceTransformerEmbeddingProviderBuilder,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)


repository = (
    JsonQuestionRepositoryBuilder.build_default(
        file_path=Path(
            "data/question_bank/questions.json"
        ),
    )
)

questions = LoadQuestionsUseCase(
    question_repository=repository,
).execute()

embedding_provider = (
    SentenceTransformerEmbeddingProviderBuilder.build_default()
)

vector_store = (
    ChromaQuestionVectorStoreBuilder.build_default()
)

indexing_service = (
    QuestionIndexingService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )
)

indexing_service.index_questions(
    questions=questions,
)

print(
    f"Indexed {len(questions)} questions."
)