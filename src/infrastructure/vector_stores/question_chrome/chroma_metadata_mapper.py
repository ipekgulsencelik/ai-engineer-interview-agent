from typing import Any

from src.domain.entities.question import Question


class ChromaMetadataMapper:
    """
    Question domain entity'sini ChromaDB metadata formatına dönüştüren
    infrastructure mapper sınıfıdır.

    Bu sınıfın temel amacı, domain entity ile vector database metadata formatı
    arasındaki dönüşümü merkezi ve güvenli şekilde yönetmektir.

    Temel fikir:
        Domain modeli:
            rich typed object

        ChromaDB metadata:
            primitive dictionary structure

        bekler.

    Bu nedenle:
        Question entity
            ↓
        provider-safe metadata dict

    dönüşümü gerekir.

    Neden gerekli?
        ChromaDB metadata alanları yalnızca primitive ve serialize edilebilir
        değerler bekler.

        Örneğin:
            - str
            - int
            - float
            - bool

        gibi değerler güvenlidir.

        Ancak domain modeli içinde:
            - Level enum
            - QuestionType enum
            - custom value object

        gibi provider açısından bilinmeyen tipler olabilir.

    Örnek problem:
        Question.level:
            Level.MID

        ChromaDB metadata:
            "MID"

        bekler.

        Eğer enum doğrudan gönderilirse:
            - serialization problemi oluşabilir
            - provider compatibility bozulabilir
            - filtering davranışı bozulabilir

    Bu mapper bu dönüşümü merkezi şekilde yönetir.

    Bu sınıf neden ayrı tutuldu?
        Eğer metadata preparation logic doğrudan ChromaVectorStore içine
        yazılırsa:

            - adapter şişer
            - metadata schema dağılır
            - dönüşüm logic'i tekrar eder
            - test izolasyonu azalır
            - provider-specific format adapter'a gömülür

        Bu nedenle metadata mapping ayrı sınıfa taşınmıştır.

    Responsibility ayrımı:
        Question:
            domain state taşır

        ChromaMetadataMapper:
            Question -> metadata dönüşümü yapar

        ChromaVectorStore:
            persistence/search işlemlerini yönetir

    Bu ayrım neden önemli?
        Çünkü:
            domain modeling
                ile
            infrastructure serialization
        farklı sorumluluklardır.

    Bu mapper ne yapar?
        - Question entity'sinden metadata dict üretir
        - enum değerlerini primitive string'e çevirir
        - provider-safe metadata üretir
        - None değerleri temizler
        - metadata schema'yı merkezi yönetir

    Bu mapper ne yapmaz?
        - ChromaDB'ye kayıt eklemez
        - embedding validation yapmaz
        - semantic search yapmaz
        - SearchResult üretmez
        - Question validation yapmaz
        - embedding üretmez

    Metadata neden önemli?
        Çünkü vector retrieval çoğu zaman:
            semantic similarity +
            metadata filtering
        kombinasyonu kullanır.

    Örnek:
        where = {
            "category": "RAG",
            "level": "MID",
        }

        Bu filtreler metadata üzerinden çalışır.

    Bu nedenle metadata formatı:
        - deterministic
        - provider-safe
        - consistent
    olmalıdır.

    Neden _remove_none_values kullanılıyor?
        Çünkü:
            gereksiz None metadata alanları

        vector store tarafında:
            - gereksiz storage
            - filtering ambiguity
            - provider incompatibility
        oluşturabilir.

    Bu mapper özellikle:
        - Chroma indexing
        - semantic retrieval filtering
        - metadata-based search
        - vector persistence
    için kritik öneme sahiptir.
    """

    @classmethod
    def from_question(
        cls,
        question: Question,
    ) -> dict[str, Any]:
        """
        Question domain entity'sinden ChromaDB metadata dict'i üretir.

        Bu metod mapper'ın ana public entry-point'idir.

        Dönüştürülen alanlar:
            - question_id
            - category
            - level
            - difficulty
            - question_type
            - market_weight
            - followup_allowed

        Neden metadata'ya tüm alanlar eklenmiyor?
            Çünkü metadata:
                retrieval/filtering amaçlıdır.

            Büyük text alanları veya karmaşık nested yapılar metadata için
            uygun olmayabilir.

        Enum alanlar neden dönüştürülüyor?
            Çünkü:
                Level.MID
                    →
                "MID"

                QuestionType.SYSTEM_DESIGN
                    →
                "system_design"

            gibi provider-safe primitive değerler gerekir.

        Neden _remove_none_values kullanılıyor?
            Çünkü:
                metadata içinde None taşımak çoğu zaman gereksizdir.

        Örnek çıktı:
            {
                "question_id": "rag_mid_001",
                "category": "RAG",
                "level": "MID",
                "difficulty": 2,
                "question_type": "conceptual",
                "market_weight": 0.8,
                "followup_allowed": True,
            }

        Bu metadata ne için kullanılabilir?
            - semantic filtering
            - analytics
            - reranking
            - retrieval debugging
            - category filtering
            - level filtering

        Args:
            question:
                Metadata'ya dönüştürülecek Question entity'si.

        Returns:
            dict[str, Any]:
                ChromaDB için güvenli primitive metadata dictionary'si.
        """

        return cls._remove_none_values(
            {
                "question_id": question.id,
                "category": question.category,
                "level": cls._to_value(question.level),
                "difficulty": question.difficulty,
                "question_type": cls._to_value(question.question_type),
                "market_weight": question.market_weight,
                "followup_allowed": question.followup_allowed,
            }
        )

    @staticmethod
    def _to_value(
        value: object,
    ) -> object:
        """
        Enum benzeri domain value objelerini primitive provider-safe değere
        dönüştürür.

        Çalışma mantığı:
            Eğer object:
                .value attribute'una sahipse

            value.value döndürülür.

            Aksi halde:
                object olduğu gibi döner.

        Bu yaklaşım neden kullanılıyor?
            Çünkü:
                - Level enum
                - QuestionType enum
                - diğer value object'ler

            primitive serialization gerektirebilir.

        Örnek:
            Level.MID
                →
            "MID"

            QuestionType.DEBUGGING
                →
            "debugging"

        Enum değilse:
            olduğu gibi döndürülür.

        Örnek:
            5
                →
            5

            "RAG"
                →
            "RAG"

        Neden generic yaklaşım tercih edildi?
            Çünkü mapper belirli enum tiplerine sıkı bağlı kalmamalıdır.

        Böylece:
            gelecekte yeni enum/value object türleri eklense bile
            mapper daha esnek çalışabilir.

        Args:
            value:
                Primitive değere dönüştürülecek object.

        Returns:
            object:
                Provider-safe primitive değer.
        """

        if hasattr(value, "value"):
            return value.value

        return value

    @staticmethod
    def _remove_none_values(
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Metadata dictionary içindeki None değerleri temizler.

        Bu helper provider'a gereksiz veya anlamsız metadata alanlarının
        gönderilmesini engeller.

        Örnek:
            input:
                {
                    "category": "RAG",
                    "level": None,
                }

            output:
                {
                    "category": "RAG",
                }

        Neden önemli?
            Bazı vector database provider'ları:
                - None metadata'yı desteklemeyebilir
                - filtering sırasında problem yaşayabilir
                - gereksiz storage kullanabilir

        Ayrıca temiz metadata:
            - daha okunabilir
            - daha deterministic
            - daha provider-safe

        hale gelir.

        Bu metod immutable-style çalışır.
        Input dictionary mutate edilmez.

        Args:
            metadata:
                Temizlenecek metadata dictionary'si.

        Returns:
            dict[str, Any]:
                None değerleri kaldırılmış metadata dictionary'si.
        """

        return {
            key: value
            for key, value in metadata.items()
            if value is not None
        }