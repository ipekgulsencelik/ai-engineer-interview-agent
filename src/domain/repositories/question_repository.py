from abc import ABC, abstractmethod

from src.domain.entities.question import Question


class QuestionRepository(ABC):
    """
    Question veri erişimi için tanımlanan repository abstraction contract'ıdır.

    Bu interface'in temel amacı, application/service katmanını veri kaynağı
    detaylarından tamamen bağımsız hale getirmektir.

    Temel fikir:
        Application layer şunu bilmemelidir:

            - veri JSON'dan mı geliyor?
            - PostgreSQL'den mi geliyor?
            - MongoDB'den mi geliyor?
            - REST API'den mi geliyor?
            - vector database'den mi geliyor?
            - memory cache'den mi geliyor?

        Application layer yalnızca şu capability ile ilgilenmelidir:

            "Question verisine erişilebiliyor mu?"

    Bu nedenle service katmanı:
        concrete storage implementation'a değil,
        repository abstraction'ına bağımlı olur.

    Bu yapı hangi mimari yaklaşımı temsil eder?
        Bu yaklaşım:
            - Repository Pattern
            - Dependency Inversion Principle
            - Clean Architecture
            - Hexagonal Architecture

        prensipleriyle uyumludur.

    Mimari rolü:
        QuestionRepository:
            application/domain port abstraction

        JsonQuestionRepository:
            infrastructure adapter

        SqlQuestionRepository:
            infrastructure adapter

        ApiQuestionRepository:
            infrastructure adapter

    Böylece application layer:
        veri kaynağını bilmeden çalışabilir.

    Neden repository abstraction gerekli?
        Eğer service katmanı doğrudan:

            open("questions.json")

        veya:

            session.query(...)

        kullanırsa:

            - infrastructure bağımlılığı oluşur
            - test yazımı zorlaşır
            - storage migration maliyetli hale gelir
            - mock repository üretmek zorlaşır
            - service katmanı şişer

    Repository abstraction bu problemleri çözer.

    Bu yaklaşımın avantajları:
        - persistence isolation
        - kolay test edilebilirlik
        - mock/fake repository desteği
        - storage bağımsızlığı
        - infrastructure değişim kolaylığı
        - cleaner service layer

    Örnek implementasyonlar:
        - JsonQuestionRepository
        - SqlAlchemyQuestionRepository
        - MongoQuestionRepository
        - ApiQuestionRepository
        - InMemoryQuestionRepository
        - CachedQuestionRepository

    Bu interface ne yapar?
        - Question erişim contract'ını tanımlar
        - application layer için ortak API sağlar

    Bu interface ne yapmaz?
        - JSON parsing yapmaz
        - database query yazmaz
        - HTTP request göndermez
        - caching yapmaz
        - persistence logic içermez
        - vector search yapmaz

    Bunlar concrete repository implementasyonlarının sorumluluğudur.

    Repository neden Question entity döndürüyor?
        Çünkü application layer infrastructure response formatlarıyla
        uğraşmamalıdır.

        Örneğin:
            raw JSON
            ORM row object
            API payload

        yerine doğrudan domain-safe Question entity döndürülür.

    Bu yaklaşım:
        - domain isolation
        - type safety
        - cleaner application logic

    sağlar.

    Test avantajı:
        Mock repository kolayca yazılabilir:

            class FakeQuestionRepository(QuestionRepository):
                ...

        Böylece:
            - database gerekmeden
            - JSON dosyası olmadan
            - hızlı unit test

        yazılabilir.
    """

    @abstractmethod
    def list_all(self) -> list[Question]:
        """
        Repository içindeki tüm Question entity'lerini döndürür.

        Bu metod application/service layer'ın tüm question bank'e erişmesini
        sağlar.

        Tipik kullanım alanları:
            - question selection
            - semantic indexing
            - retrieval preparation
            - analytics
            - admin tooling
            - CLI debugging

        Önemli:
            Bu metod yalnızca domain-safe Question entity'leri döndürmelidir.

            Raw infrastructure formatları:
                - dict
                - JSON payload
                - ORM row
                - SQL result

            application layer'a sızmamalıdır.

        Concrete repository implementasyonları:
            - JSON okuyabilir
            - database query çalıştırabilir
            - API request gönderebilir
            - cache kullanabilir

        Ancak caller bunları bilmez.

        Returns:
            list[Question]:
                Repository içindeki tüm Question entity'leri.

        Raises:
            NotImplementedError:
                Abstract interface doğrudan kullanılırsa fırlatılır.
        """
        raise NotImplementedError


    @abstractmethod
    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """
        Verilen question_id değerine sahip Question entity'sini döndürür.

        Bu metod question lookup işlemleri için kullanılır.

        Tipik kullanım alanları:
            - interview replay
            - follow-up generation
            - analytics lookup
            - question detail inspection
            - duplicate detection

        Question bulunamazsa neden None dönüyor?
            Çünkü:
                "question mevcut değil"

            durumu normal bir business senaryosudur.

            Bu nedenle exception yerine:
                None

            dönmek daha uygundur.

        Örnek:
            question = repository.get_by_id("rag_jr_001")

            if question is None:
                ...

        Bu yaklaşım:
            - daha sade flow control
            - daha okunabilir service logic
            - predictable repository behavior

        sağlar.

        Args:
            question_id:
                Aranacak Question entity id değeri.

        Returns:
            Question | None:
                İlgili Question entity'si.

                Eğer bulunamazsa:
                    None

        Raises:
            NotImplementedError:
                Abstract interface doğrudan kullanılırsa fırlatılır.
        """
        raise NotImplementedError