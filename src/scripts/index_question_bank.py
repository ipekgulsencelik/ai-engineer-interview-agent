from pathlib import Path

from src.application.services.question_indexing_service import (
    QuestionIndexingService,
)
from src.application.use_cases.load_question_bank_use_case import (
    LoadQuestionBankUseCase,
)
from src.infrastructure.embeddings.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.vector_store.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)

repository = JsonQuestionRepository(
    file_path=Path(
        "data/question_bank/questions.json"
    ),
)

questions = (
    LoadQuestionBankUseCase(
        question_repository=repository,
    ).execute()
)

embedding_model = (
    SentenceTransformerEmbeddingModel()
)

vector_store = (
    ChromaQuestionVectorStore()
)

indexing_service = (
    QuestionIndexingService(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )
)

indexing_service.index_questions(
    questions,
)

print(
    f"Indexed {len(questions)} questions."
)