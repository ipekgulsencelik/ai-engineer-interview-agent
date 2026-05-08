from src.config.settings import settings
from src.infrastructure.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.evaluator.groq_rubric_evaluator import (
    GroqRubricEvaluator,
)
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.vector_stores.chroma_vector_store import (
    ChromaVectorStore,
)
from src.logging.logger import (
    configure_logging,
)
from src.services.follow_up_generation_service import (
    FollowUpGenerationService,
)
from src.services.level_transition_service import (
    LevelTransitionService,
)
from src.services.question_retrieval_service import (
    QuestionRetrievalService,
)


class Container:
    """
    Merkezi dependency injection container.

    Bu class'ın amacı:
        Uygulamanın tüm dependency wiring işlemlerini merkezi ve kontrollü
        şekilde yönetmektir.

    Dependency Injection (DI) neden önemlidir?
        Çünkü production-grade sistemlerde object'lerin dependency'lerini
        kendi içerisinde oluşturması:
            - tight coupling
            - zor test edilebilirlik
            - düşük maintainability
            - rigid architecture

        oluşturur.

    DI Container yaklaşımı sayesinde:
        ✔ centralized object creation
        ✔ loose coupling
        ✔ easier testing
        ✔ cleaner composition root
        ✔ configurable infrastructure
        ✔ easier mocking
        ✔ lifecycle management

    Bu container ne yapar?
        ✔ infrastructure object creation
        ✔ service wiring
        ✔ centralized configuration usage
        ✔ dependency composition

    Bu container ne yapmaz?
        ✘ business logic
        ✘ orchestration
        ✘ runtime processing
        ✘ request handling
        ✘ evaluation
        ✘ retrieval execution

    Çünkü görevi yalnızca:
        object graph composition

    yapmaktır.

    Mimari yaklaşım:
        Settings
            ↓
        Container
            ↓
        Infrastructure + Services
            ↓
        UseCases / Pipelines

    Bu yapı neden değerlidir?
        Çünkü:
            object creation logic

        business logic'ten ayrılmış olur.

    Örnek:
        Kötü yaklaşım:
            service içinde 직접 GroqRubricEvaluator() oluşturmak

        İyi yaklaşım:
            container üzerinden dependency inject etmek

    Böylece:
        - mock object inject etmek kolaylaşır
        - provider değiştirmek kolaylaşır
        - lifecycle yönetimi merkezileşir

    Önemli mimari not:
        Bu container şu an:
            manual dependency injection

        yaklaşımı kullanıyor.

    Production-scale alternatifler:
        - dependency-injector
        - punq
        - lagom
        - wired
        - FastAPI DI system
    kullanılabilir.

    Şu anki yaklaşım Faz-1 için:
        ✔ basit
        ✔ okunabilir
        ✔ yeterince maintainable

    Singleton davranışı var mı?
        Şu an:
            her build çağrısı yeni instance üretir.

    Örneğin:
        self.build_vector_store()

    her çağrıldığında yeni ChromaVectorStore oluşur.

    Daha gelişmiş lifecycle yönetiminde:
        - singleton
        - scoped
        - transient

    lifecycle'lar eklenebilir.

    Gelecekte eklenebilecek geliştirmeler:
        - singleton caching
        - lazy initialization
        - async providers
        - provider registry
        - environment-aware wiring
        - test container
        - mock overrides
        - lifecycle scopes
    """

    def __init__(self) -> None:
        configure_logging()

    # ---------------------------------------------------------
    # EMBEDDING MODEL
    # ---------------------------------------------------------
    def build_embedding_model(
        self,
    ) -> SentenceTransformerEmbeddingModel:
        """
        SentenceTransformer tabanlı embedding model instance'ı oluşturur.

        Returns:
            SentenceTransformerEmbeddingModel:
                Semantic embedding üretimi için kullanılacak model.

        Design Note:
            Model adı centralized settings üzerinden alınır.

            Böylece:
                embedding backend değiştirmek için
                kod değişikliği gerekmez.
        """

        return SentenceTransformerEmbeddingModel(
            model_name=(settings.EMBEDDING_MODEL_NAME)
        )

    # ---------------------------------------------------------
    # VECTOR STORE
    # ---------------------------------------------------------
    def build_vector_store(
        self,
    ) -> ChromaVectorStore:
        """
        ChromaDB tabanlı vector store instance'ı oluşturur.

        Returns:
            ChromaVectorStore:
                Semantic vector persistence ve retrieval sistemi.

        Kullanım alanları:
            - semantic search
            - nearest-neighbor retrieval
            - embedding indexing

        Design Note:
            Collection ve persistence config'i centralized settings üzerinden
            alınır.
        """

        return ChromaVectorStore(
            collection_name=(settings.CHROMA_COLLECTION_NAME),
            persist_directory=(settings.CHROMA_PERSIST_DIR),
        )

    # ---------------------------------------------------------
    # QUESTION REPOSITORY
    # ---------------------------------------------------------
    def build_question_repository(
        self,
    ) -> JsonQuestionRepository:
        """
        JSON tabanlı question repository instance'ı oluşturur.

        Returns:
            JsonQuestionRepository:
                Question dataset erişim katmanı.

        Bu repository:
            - question loading
            - question lookup
            - dataset retrieval

        işlemlerini gerçekleştirir.
        """

        return JsonQuestionRepository(json_path=(settings.QUESTION_DATA_PATH))

    # ---------------------------------------------------------
    # RETRIEVAL SERVICE
    # ---------------------------------------------------------
    def build_question_retrieval_service(
        self,
    ) -> QuestionRetrievalService:
        """
        Semantic question retrieval service instance'ı oluşturur.

        Bu service:
            - embedding generation
            - vector similarity search
            - Question retrieval

        işlemlerini orkestre eder.

        Dependency graph:
            QuestionRetrievalService
                ├── EmbeddingModel
                ├── VectorStore
                └── QuestionRepository

        Returns:
            QuestionRetrievalService:
                Semantic retrieval orchestration service.

        Design Note:
            Bu method nested dependency wiring yapmaktadır.

            Böylece retrieval service ihtiyaç duyduğu tüm dependency'lerle
            hazır şekilde döndürülür.
        """

        return QuestionRetrievalService(
            embedding_model=(self.build_embedding_model()),
            vector_store=(self.build_vector_store()),
            repository=(self.build_question_repository()),
        )

    # ---------------------------------------------------------
    # LEVEL TRANSITION SERVICE
    # ---------------------------------------------------------
    def build_level_transition_service(
        self,
    ) -> LevelTransitionService:
        """
        Candidate level transition service instance'ı oluşturur.

        Bu service:
            Candidate score history'ye göre:
                - level up
                - level down
                - level 유지

            kararları verir.

        Returns:
            LevelTransitionService:
                Adaptive level transition service.
        """

        return LevelTransitionService()

    # ---------------------------------------------------------
    # GROQ EVALUATOR
    # ---------------------------------------------------------
    def build_groq_evaluator(
        self,
    ) -> GroqRubricEvaluator:
        """
        Groq tabanlı rubric evaluator instance'ı oluşturur.

        Bu evaluator:
            - candidate answer evaluation
            - rubric scoring
            - structured feedback generation

        işlemlerini gerçekleştirir.

        Returns:
            GroqRubricEvaluator:
                Gerçek LLM tabanlı evaluator implementation.

        Design Note:
            API key ve model config'i evaluator içerisinde settings üzerinden
            alınmaktadır.
        """

        return GroqRubricEvaluator()

    # ---------------------------------------------------------
    # FOLLOW-UP GENERATION SERVICE
    # ---------------------------------------------------------
    def build_follow_up_generation_service(
        self,
    ) -> FollowUpGenerationService:
        """
        Adaptive follow-up generation service instance'ı oluşturur.

        Bu service:
            Candidate answer'a göre:
                - intelligent probing
                - missing concept exploration
                - adaptive questioning

            yapar.

        Returns:
            FollowUpGenerationService:
                Dynamic follow-up generation service.

        Kullanım alanları:
            - conversational interview flow
            - deep technical probing
            - adaptive assessment systems
        """

        return FollowUpGenerationService()
