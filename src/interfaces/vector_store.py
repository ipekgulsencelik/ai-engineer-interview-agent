from abc import ABC, abstractmethod

from src.domain.search.search_result import SearchResult


class VectorStore(ABC):
    """
    Semantic search / vector database abstraction.

    Bu sınıf doğrudan çalışan somut bir vector database implementasyonu değildir.
    Bunun yerine embedding tabanlı semantic search sistemleri için ortak bir
    contract tanımlar.

    Amaç:
        Application/service katmanının belirli bir vector database teknolojisine
        doğrudan bağımlı olmasını engellemektir.

    Bu abstraction sayesinde sistem:
        - ChromaDB
        - Pinecone
        - Weaviate
        - Qdrant
        - FAISS
        - pgvector
        - Elasticsearch vector search

    gibi farklı vector backend'leri aynı interface üzerinden kullanabilir.

    Bu interface'in temel sorumlulukları:
        - embedding'e karşılık gelen text kayıtlarını saklamak
        - semantic similarity search yapmak
        - metadata bazlı filtreleme desteklemek

    Kullanım alanları:
        - semantic question retrieval
        - benzer soru bulma
        - follow-up question retrieval
        - duplicate detection
        - semantic diversity scoring
        - RAG retrieval
        - interview memory search

    Mimari konum:
        Application/Service layer:
            QuestionRetrievalService
            SemanticSearchService
            SimilarityService

        Interface:
            VectorStore

        Infrastructure implementations:
            ChromaVectorStore
            PineconeVectorStore
            FAISSVectorStore
            InMemoryVectorStore

    Neden abstraction kullanıyoruz?
        - Vector database provider bağımlılığı azalır.
        - Provider değiştirmek kolaylaşır.
        - Testlerde fake vector store kullanılabilir.
        - Semantic retrieval logic infrastructure'dan ayrılır.
        - Dependency Inversion Principle uygulanır.
        - Retrieval pipeline daha modüler hale gelir.

    Önemli tasarım notu:
        Bu interface embedding modelini yönetmez.

        Yani burada:
            - sentence-transformers encode işlemi
            - OpenAI embedding API çağrısı
            - embedding dimension yönetimi
            - tokenizer işlemleri

        bulunmamalıdır.

        Embedding üretme sorumluluğu ayrı bir EmbeddingModel abstraction'ına
        ait olmalıdır.

    Bu interface yalnızca:
        - vector kayıt ekleme
        - semantic retrieval
        işlemlerini tanımlar.

    Beklenen davranış:
        Vector store text + metadata kayıtlarını embedding space içerisinde
        saklar ve semantic similarity üzerinden retrieval yapar.

    Örnek akış:
        text
            ↓
        embedding model
            ↓
        vector
            ↓
        VectorStore.add(...)

        search query
            ↓
        embedding model
            ↓
        query vector
            ↓
        VectorStore.search(...)

    Not:
        Bu interface bilinçli olarak küçük tutulmuştur.

        İlerleyen fazlarda:
            - delete
            - update
            - batch_add
            - hybrid_search
            - reranking
            - namespace support
            - score threshold

        gibi advanced retrieval özellikleri eklenebilir.
    """

    @abstractmethod
    def add(
        self,
        id: str,
        text: str,
        metadata: dict,
    ) -> None:
        """
        Vector store içerisine yeni bir text kaydı ekler.

        Bu method genellikle indexing pipeline sırasında kullanılır.

        Örnek akış:
            1. Question repository'den soru okunur.
            2. Question text embedding'e dönüştürülür.
            3. Embedding + metadata vector store'a eklenir.

        Eklenen kayıtlar daha sonra semantic retrieval sırasında kullanılabilir.

        Args:
            id:
                Kaydın unique identifier değeridir.

                Örnek:
                    "rag_jr_001"
                    "embedding_mid_004"

                Bu id genellikle:
                    - question id
                    - document id
                    - chunk id

                olabilir.

                Aynı id'nin tekrar eklenmesi provider implementasyonuna göre:
                    - overwrite
                    - ignore
                    - exception
                    davranışı gösterebilir.

            text:
                Embedding'e karşılık gelen ham metin içeriğidir.

                Örnek:
                    - question text
                    - document chunk
                    - interview memory
                    - RAG paragraph

                Semantic retrieval sırasında kullanıcı query'si bu metinlerle
                similarity karşılaştırmasına girer.

            metadata:
                Kayıt hakkında ek filtreleme bilgilerini içerir.

                Örnek:
                    {
                        "category": "RAG",
                        "level": "MID",
                        "difficulty": 2,
                        "question_type": "scenario"
                    }

                Metadata semantic search sırasında filter amaçlı kullanılabilir.

                Örnek:
                    where={"category": "RAG"}

        Returns:
            None:
                Method başarılı olursa değer döndürmez.

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan VectorStore üzerinden
                çağrılamaz. Mutlaka somut bir subclass tarafından implemente
                edilmelidir.

            ValueError:
                Somut implementasyonlar:
                    - boş id
                    - boş text
                    - geçersiz metadata
                durumlarında ValueError fırlatabilir.

            RuntimeError:
                Vector database bağlantı hataları, indexing problemleri veya
                provider API hataları RuntimeError benzeri uygulama seviyesinde
                anlamlı exception'lara dönüştürülebilir.

        Design Note:
            Bu method embedding üretmemelidir.

            Yanlış yaklaşım:
                VectorStore içinde embedding model çağırmak.

            Doğru yaklaşım:
                Embedding ayrı katmanda üretilir,
                VectorStore yalnızca storage/retrieval işlemi yapar.

            Böylece:
                - separation of concerns korunur
                - farklı embedding modelleri desteklenebilir
                - vector backend bağımsız kalır
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """
        Verilen query için semantic similarity tabanlı arama yapar.

        Bu method keyword search değil semantic/vector search yapar.

        Yani sistem:
            - exact kelime eşleşmesine değil
            - embedding similarity'ye göre

        sonuç döndürür.

        Örnek:
            Query:
                "How do embeddings work?"

            Semantic olarak benzer sonuçlar:
                - vector representation soruları
                - embedding architecture soruları
                - similarity search soruları

        olabilir.

        Args:
            query:
                Semantic search için kullanılacak doğal dil query'sidir.

                Örnek:
                    "RAG retrieval optimization"
                    "How vector databases work"
                    "LLM evaluation metrics"

                Bu query embedding'e dönüştürülerek vector similarity
                karşılaştırmasında kullanılır.

            limit:
                Döndürülecek maksimum sonuç sayısını belirler.

                Varsayılan:
                    5

                Örnek:
                    limit=3 -> en benzer ilk 3 sonuç döner.

            where:
                Opsiyonel metadata filtreleme koşuludur.

                Örnek:
                    {"category": "RAG"}
                    {"level": "MID"}

                Böylece semantic retrieval belirli alt kümelerle
                sınırlandırılabilir.

                Kullanım örnekleri:
                    - sadece MID sorular
                    - sadece coding soruları
                    - sadece RAG kategorisi

        Returns:
            list[SearchResult]:
                Semantic similarity skoruna göre sıralanmış retrieval sonuçları.

                Her SearchResult genellikle:
                    - text
                    - metadata
                    - similarity score
                    - source id

                gibi alanlar içerir.

                Sonuçlar genellikle:
                    en yüksek similarity
                        ↓
                    en düşük similarity

                şeklinde sıralanır.

                Hiç sonuç bulunamazsa boş liste dönebilir.

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan VectorStore üzerinden
                çağrılamaz. Mutlaka somut bir subclass tarafından implemente
                edilmelidir.

            ValueError:
                Somut implementasyonlar boş query veya geçersiz limit
                durumlarında ValueError fırlatabilir.

            RuntimeError:
                Vector database erişim problemleri, query timeout veya
                provider hataları RuntimeError seviyesinde exception'lara
                dönüştürülebilir.

        Design Note:
            Bu interface retrieval contract'ını tanımlar.

            Şunlar burada olmamalıdır:
                - reranking logic
                - answer generation
                - prompt construction
                - LLM çağrıları
                - business scoring logic

            Bu sorumluluklar:
                - retrieval service
                - ranking service
                - RAG pipeline
                - orchestration layer

            içerisinde yönetilmelidir.

        Example:
            results = vector_store.search(
                query="How does RAG retrieval work?",
                limit=3,
                where={"level": "MID"},
            )

            for result in results:
                print(result.text)
                print(result.score)
        """
        pass
