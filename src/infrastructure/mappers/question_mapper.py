from __future__ import annotations

from typing import Any, Mapping

from src.domain.constants.question import (
    DEFAULT_FOLLOWUP_ALLOWED,
    DEFAULT_MARKET_WEIGHT,
)
from src.domain.entities.question import Question
from src.domain.factories.question_factory import (
    QuestionFactory,
)


class QuestionMapper:
    """
    Raw mapping payload verisini domain-safe Question entity'sine
    dönüştüren minimal infrastructure mapper sınıfıdır.

    Bu mapper intentionally lightweight tutulmuştur.

    Çünkü:
        domain invariant validation responsibility'si
        QuestionFactory + Question entity + QuestionValidator
        tarafındadır.

    ----------------------------------------------------------------------
    NEDEN MAPPER VAR?
    ----------------------------------------------------------------------

    External veri kaynakları genellikle primitive payload üretir.

    Örneğin:

        - JSON dosyaları
        - repository output'ları
        - seed data
        - API payload'ları

    Bu payload'lar doğrudan domain entity değildir.

    QuestionMapper:
        raw payload ile domain model arasında translation/adaptation
        katmanı görevi görür.

    ----------------------------------------------------------------------
    RESPONSIBILITY BOUNDARY
    ----------------------------------------------------------------------

    Bu mapper:

        ✔ payload field'larını okur
        ✔ QuestionFactory'ye aktarır
        ✔ optional field default'larını uygular

    Bu mapper:

        ✘ domain validation yapmaz
        ✘ invariant yönetmez
        ✘ normalization yapmaz
        ✘ persistence işlemi yapmaz
        ✘ scoring yapmaz
        ✘ business logic çalıştırmaz

    ----------------------------------------------------------------------
    NEDEN VALIDATION YOK?
    ----------------------------------------------------------------------

    Bu bilinçli bir architectural tercihtir.

    Çünkü validation responsibility:
        domain katmanında merkezi kalmalıdır.

    Eğer mapper validation yaparsa:

        - validation duplication oluşabilir
        - domain rule'ları infrastructure'a sızabilir
        - SRP zayıflayabilir
        - inconsistent validation behavior oluşabilir

    Bu nedenle:
        mapper yalnızca translation responsibility taşır.

    ----------------------------------------------------------------------
    DEFAULT VALUE STRATEJİSİ
    ----------------------------------------------------------------------

    Bazı optional alanlar payload içinde bulunmayabilir.

    Örneğin:
        market_weight
        followup_allowed

    Bu durumda domain default değerleri uygulanır:

        DEFAULT_MARKET_WEIGHT
        DEFAULT_FOLLOWUP_ALLOWED

    Böylece:
        payload eksik olsa bile QuestionFactory deterministic şekilde
        çalışabilir.

    ----------------------------------------------------------------------
    QUESTIONFACTORY KULLANIMI
    ----------------------------------------------------------------------

    Mapper doğrudan Question(...) oluşturmaz.

    Bunun yerine:

        QuestionFactory.create(...)

    çağırır.

    Bu yaklaşım önemlidir çünkü:

        - object creation merkezi hale gelir
        - future creation policy'leri kolaylaşır
        - normalization eklemek kolay olur
        - validation flow korunur

    ----------------------------------------------------------------------
    DESIGN FELSEFESİ
    ----------------------------------------------------------------------

    Bu versiyon intentionally minimalist tutulmuştur.

    Çünkü:
        aşırı abstraction her zaman daha iyi mimari anlamına gelmez.

    Eğer:
        - payload shape stabil ise
        - transformation logic basitse
        - ekstra orchestration yoksa

    lightweight mapper daha maintainable olabilir.

    ----------------------------------------------------------------------
    INFRASTRUCTURE LAYER NOTU
    ----------------------------------------------------------------------

    Bu sınıf domain layer'da değil,
    infrastructure/application boundary'sinde konumlandırılmalıdır.

    Çünkü:
        raw payload formatını bilir.

    Domain entity:
        JSON shape veya repository structure bilmemelidir.
    """

    @staticmethod
    def from_mapping(
        payload: Mapping[str, Any],
        index: int,
    ) -> Question:
        """
        Raw mapping payload üzerinden Question entity üretir.

        Bu method:
            primitive dictionary/mapping verisini
            domain-safe Question entity'sine dönüştürür.

        ------------------------------------------------------------------
        PAYLOAD ÖRNEĞİ
        ------------------------------------------------------------------

            {
                "id": "rag_jr_001",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "JR",
                "difficulty": 1,
                "question_type": "conceptual",
                "expected_points": ["retrieval"],
                "keywords": ["rag"],
            }

        ------------------------------------------------------------------
        OPTIONAL FIELD DAVRANIŞI
        ------------------------------------------------------------------

        Payload içinde bazı alanlar bulunmazsa:

            market_weight
            followup_allowed

        için default domain değerleri uygulanır.

        Böylece:
            incomplete payload'lar deterministic şekilde işlenebilir.

        ------------------------------------------------------------------
        VALIDATION NOTU
        ------------------------------------------------------------------

        Bu method explicit validation yapmaz.

        Çünkü:
            domain-safe validation responsibility'si
            QuestionFactory / Question / QuestionValidator
            zincirindedir.

        Invalid payload durumunda:
            ilgili exception'lar domain layer'dan gelir.

        ------------------------------------------------------------------
        Args
        ------------------------------------------------------------------

        payload:
            Raw mapping/dictionary veri.

        ------------------------------------------------------------------
        Returns
        ------------------------------------------------------------------

        Question:
            Immutable ve domain-safe Question entity'si.
        """
        try:

            return QuestionFactory.create(
                id=payload["id"],
                text=payload["text"],
                category=payload["category"],
                level=payload["level"],
                difficulty=payload["difficulty"],
                question_type=payload["question_type"],

                # ----------------------------------------------------------
                # OPTIONAL DOMAIN FIELDS
                # ----------------------------------------------------------
                #
                # Bu alanlar payload içinde bulunmayabilir.
                #
                # None/default davranışı:
                #   QuestionFactory + Question entity tarafından yönetilir.
                #
                expected_points=payload.get(
                    "expected_points",
                ),

                keywords=payload.get(
                    "keywords",
                ),

                # ----------------------------------------------------------
                # DEFAULT MARKET WEIGHT
                # ----------------------------------------------------------
                #
                # Payload içinde market_weight yoksa:
                #   domain default değeri kullanılır.
                #
                market_weight=payload.get(
                    "market_weight",
                    DEFAULT_MARKET_WEIGHT,
                ),

                # ----------------------------------------------------------
                # DEFAULT FOLLOW-UP POLICY
                # ----------------------------------------------------------
                #
                # Payload explicit follow-up behavior belirtmiyorsa:
                #   domain default strategy uygulanır.
                #
                followup_allowed=payload.get(
                    "followup_allowed",
                    DEFAULT_FOLLOWUP_ALLOWED,
                ),
            )
        except Exception as error:
            raise ValueError(
                f"Invalid question record at index {index} "
                f"(id={payload.get('id')}): {error}"
            ) from error