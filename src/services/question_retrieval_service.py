from src.domain.question.question import Question
from src.infrastructure.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.repositories.json_question_repository import (
    JsonQuestionRepository,
)
from src.infrastructure.vector_stores.chroma_vector_store import (
    ChromaVectorStore,
)
from src.logging.logger import logger


class QuestionRetrievalService:
    """
    Semantic question retrieval orchestration service.

    Bu service'in amacı:
        Kullanıcının doğal dil query'sine semantic olarak en yakın interview
        sorularını bulmak ve Question domain modeli olarak döndürmektir.

    Bu service klasik keyword search yapmaz.

    Bunun yerine:
        query text
            ↓
        embedding vector
            ↓
        vector similarity search
            ↓
        SearchResult
            ↓
        Question domain model

    akışını yönetir.

    Neden semantic retrieval gerekli?
        Çünkü interview sisteminde kullanıcı query'si ile soru metni birebir
        aynı kelimeleri içermeyebilir.

        Örnek:
            Query:
                "How can we improve retrieval quality?"

            İlgili soru:
                "What strategies can be used to optimize RAG retrieval?"

        Keyword eşleşmesi zayıf olabilir.
        Ancak semantic similarity yüksek olabilir.

    Bu service ne yapar?
        ✔ Question dataset'ini vector store'a indexler
        ✔ Question text için embedding üretir
        ✔ Query embedding üretir
        ✔ ChromaDB üzerinden semantic search yapar
        ✔ SearchResult id'lerini Question domain modeline map eder

    Bu service ne yapmaz?
        ✘ Embedding algoritması implemente etmez
        ✘ Vector database detaylarını bilmez
        ✘ Question JSON parse logic içermez
        ✘ LLM çağırmaz
        ✘ Answer evaluation yapmaz
        ✘ Question scoring yapmaz

    Mimari konum:
        Application Service:
            QuestionRetrievalService

        Infrastructure:
            SentenceTransformerEmbeddingModel
            ChromaVectorStore
            JsonQuestionRepository

    Önemli tasarım notu:
        Bu service şu an somut infrastructure class'larına bağımlı.

        Daha senior/clean architecture yaklaşımında constructor şunları
        interface olarak almalıdır:
            - EmbeddingModel
            - VectorStore
            - QuestionRepository

        Böylece service infrastructure detaylarından daha iyi izole edilir.

    Faz-1 için mevcut hali çalışır ve anlaşılırdır.
    Faz-2'de abstraction'lara çekilmesi daha doğru olur.

    Kullanım senaryoları:
        - Kullanıcının query'sine göre benzer soruları bulmak
        - CV skill'lerine göre ilgili soruları retrieve etmek
        - Weak area için hedefli soru bulmak
        - Semantic duplicate detection yapmak
        - RAG tabanlı question selection pipeline oluşturmak

    Örnek kullanım:
        service = QuestionRetrievalService(
            embedding_model=SentenceTransformerEmbeddingModel(),
            vector_store=ChromaVectorStore(),
            repository=JsonQuestionRepository("data/questions.json"),
        )

        service.index_questions()

        questions = service.retrieve(
            query="Explain RAG retrieval optimization",
            limit=3,
        )
    """

    def __init__(
        self,
        embedding_model: SentenceTransformerEmbeddingModel,
        vector_store: ChromaVectorStore,
        repository: JsonQuestionRepository,
    ) -> None:
        """
        QuestionRetrievalService instance'ı oluşturur.

        Args:
            embedding_model:
                Text verisini embedding vector'e dönüştüren model.

                Bu implementation şu an:
                    SentenceTransformerEmbeddingModel

                olarak verilmiştir.

            vector_store:
                Embedding vector'lerini saklayan ve semantic similarity search
                yapan vector database abstraction/implementation.

                Bu implementation şu an:
                    ChromaVectorStore

                olarak verilmiştir.

            repository:
                Question dataset'ini sağlayan repository.

                Bu implementation şu an:
                    JsonQuestionRepository

                olarak verilmiştir.

        Design Note:
            Bu üç dependency birlikte semantic retrieval pipeline'ını oluşturur.

            embedding_model:
                text → vector

            vector_store:
                vector → nearest neighbors

            repository:
                id → Question

            şeklinde çalışır.
        """

        # ---------------------------------------------------------
        # DEPENDENCY ASSIGNMENT
        # ---------------------------------------------------------
        # Semantic retrieval pipeline için gerekli bileşenler saklanır.
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.repository = repository

    def index_questions(self) -> None:
        """
        Repository içerisindeki tüm question dataset'ini vector store'a indexler.

        Bu method genellikle uygulama başlangıcında veya ingestion script'i
        içerisinde çalıştırılır.

        Akış:
            1. Repository'den tüm sorular alınır.
            2. Her question text için embedding üretilir.
            3. Question metadata'sı hazırlanır.
            4. Text + metadata + embedding vector store'a eklenir.

        Neden indexleme gerekiyor?
            Semantic search yapabilmek için question text'lerinin embedding
            vector'lerinin önceden vector store'a yazılmış olması gerekir.

        Returns:
            None

        Raises:
            Repository, embedding model veya vector store kaynaklı hatalar
            üst katmana propagate olabilir.

        Design Note:
            Faz-1'de her soru tek tek embed edilip indexlenmektedir.

            Daha performanslı yaklaşım:
                - embed_batch kullanmak
                - batch vector insert yapmak
                - duplicate id kontrolü yapmak
                - index versioning eklemek

            olacaktır.
        """

        logger.info(
            "question_indexing_started",
        )

        # ---------------------------------------------------------
        # LOAD QUESTIONS
        # ---------------------------------------------------------
        # Question dataset'i repository üzerinden yüklenir.
        #
        # Repository:
        #   JSON, database veya başka bir storage backend olabilir.
        questions = self.repository.list_all()

        # ---------------------------------------------------------
        # INDEX EACH QUESTION
        # ---------------------------------------------------------
        # Her question için:
        #   - text embedding üretilir
        #   - metadata hazırlanır
        #   - Chroma vector store'a eklenir
        for question in questions:
            logger.info(
                "question_indexed",
                question_id=question.id,
                category=question.category,
            )

            embedding = self.embedding_model.embed(question.text)

            self.vector_store.add(
                id=question.id,
                text=question.text,
                metadata={
                    "category": question.category,
                    "level": str(question.level),
                },
                embedding=embedding,
            )

        logger.info(
            "question_indexing_completed",
            total_questions=len(questions),
        )

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Question]:
        """
        Kullanıcı query'sine göre semantic similarity tabanlı question
        retrieval yapar.

        Akış:
            1. Query validation yapılır.
            2. Query embedding'e dönüştürülür.
            3. Vector store üzerinde semantic search yapılır.
            4. SearchResult id'leri Question domain modeline map edilir.
            5. Retrieved Question listesi döndürülür.

        Args:
            query:
                Kullanıcının doğal dil arama sorgusu.

                Örnek:
                    "RAG retrieval optimization"
                    "How do embeddings work?"
                    "Vector database scaling"

            limit:
                Döndürülecek maksimum question sayısı.

                Varsayılan:
                    5

        Returns:
            list[Question]:
                Semantic olarak query'ye en yakın Question domain modelleri.

                Sonuç sırası vector store similarity sırasını takip eder.

        Raises:
            ValueError:
                query boş veya yalnızca whitespace içeriyorsa fırlatılır.

        Design Note:
            Vector store SearchResult döndürür.
            Ancak application layer genellikle Question domain modeliyle
            çalışmak ister.

            Bu yüzden result.id üzerinden repository'deki Question objelerine
            map edilir.
        """

        # ---------------------------------------------------------
        # QUERY VALIDATION
        # ---------------------------------------------------------
        # Boş query semantic retrieval için anlamlı değildir.
        #
        # strip() kullanılarak whitespace-only query de engellenir.
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        logger.info(
            "semantic_retrieval_started",
            query=query,
            limit=limit,
        )

        # ---------------------------------------------------------
        # QUERY EMBEDDING
        # ---------------------------------------------------------
        # Doğal dil query'si embedding vector'e dönüştürülür.
        #
        # Bu vector daha sonra ChromaDB similarity search için kullanılır.
        query_embedding = self.embedding_model.embed(query)

        # ---------------------------------------------------------
        # SEMANTIC VECTOR SEARCH
        # ---------------------------------------------------------
        # Query embedding ile vector store üzerinde nearest-neighbor search
        # yapılır.
        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        logger.info(
            "semantic_search_completed",
            result_count=len(search_results),
        )

        # ---------------------------------------------------------
        # LOAD QUESTION DOMAIN OBJECTS
        # ---------------------------------------------------------
        # SearchResult yalnızca id/text/score/metadata taşıyabilir.
        #
        # Fakat üst katmana tam Question domain modeli döndürmek için
        # repository'den tüm soru dataset'i alınır.
        questions = self.repository.list_all()

        # ---------------------------------------------------------
        # QUESTION MAP CREATION
        # ---------------------------------------------------------
        # O(1) lookup için question id → Question map oluşturulur.
        #
        # Bu yaklaşım her SearchResult için listede tekrar tekrar arama
        # yapmaktan daha verimlidir.
        question_map = {question.id: question for question in questions}

        # ---------------------------------------------------------
        # SEARCH RESULT TO QUESTION MAPPING
        # ---------------------------------------------------------
        # Vector store'dan dönen result id'leri Question domain modeline
        # dönüştürülür.
        #
        # Eğer herhangi bir id repository'de bulunamazsa:
        #   sessizce atlanır.
        #
        # Bu durum:
        #   stale vector index
        #   silinmiş question
        #   repository/vector store mismatch
        #
        # durumlarında oluşabilir.
        retrieved_questions: list[Question] = []

        for result in search_results:
            question = question_map.get(result.id)

            if question is not None:
                retrieved_questions.append(question)

        logger.info(
            "question_retrieval_completed",
            retrieved_questions=len(retrieved_questions),
        )

        # ---------------------------------------------------------
        # FINAL RETRIEVED QUESTIONS
        # ---------------------------------------------------------
        # Semantic similarity sırasını koruyan Question listesi döndürülür.
        return retrieved_questions
