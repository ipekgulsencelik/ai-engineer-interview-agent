from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticRelevance:
    """
    Question bazlı semantic relevance skorlarını taşıyan immutable runtime
    snapshot modelidir.

    Bu modelin amacı, semantic retrieval veya embedding tabanlı relevance
    analizlerinden elde edilen skorları scoring engine'e aktarmaktır.

    Temel fikir:
        Interview question selection yalnızca:
            - market_weight
            - difficulty
            - category coverage

        gibi statik sinyallere göre yapılmamalıdır.

        Aynı zamanda:
            - candidate CV'si
            - önceki cevaplar
            - weak area'lar
            - retrieval query'si
            - interview amacı

        ile semantik olarak ilişkili sorular da öne çıkarılabilir.

    Semantic relevance neyi temsil eder?
        Bir sorunun mevcut interview context ile:
            - anlamsal
            - teknik
            - içeriksel

        yakınlığını temsil eder.

    Örnek:
        Candidate CV'sinde:
            - RAG
            - vector database
            - semantic search

        deneyimi varsa:

            embedding veya retrieval soruları

        daha yüksek semantic relevance alabilir.

    Bu model neden gerekli?
        Semantic retrieval sonuçları çoğu zaman:
            - vector database
            - embedding service
            - retrieval pipeline

        gibi infrastructure katmanlarında üretilir.

        Ancak scoring engine:
            yalnızca "hangi soru ne kadar alakalı?"
        bilgisini bilmek ister.

    Bu nedenle semantic scoring sonucu:
        sade ve immutable bir snapshot modele dönüştürülür.

    Bu model ne yapar?
        - semantic relevance skorlarını taşır
        - question_id bazlı erişim sağlar
        - scoring engine'e retrieval sinyali sunar

    Bu model ne yapmaz?
        - embedding üretmez
        - vector search çalıştırmaz
        - similarity hesaplamaz
        - reranking yapmaz
        - retrieval query üretmez
        - scoring yapmaz

    Semantic computation neden burada değil?
        Çünkü bu model yalnızca runtime snapshot temsil eder.

        Semantic computation logic:
            - retrieval service
            - vector store
            - reranker
            - embedding pipeline

        içinde bulunmalıdır.

    Bu ayrım neden önemlidir?
        Çünkü:
            retrieval computation
                ile
            runtime state representation

        farklı sorumluluklardır.

    Immutable tasarım:
        frozen=True kullanılmıştır.

        Çünkü semantic relevance scoring sırasında:
            deterministic
            reproducible
            side-effect free

        olmalıdır.

        Eğer runtime sırasında relevance map mutate edilirse:
            - scoring davranışı değişebilir
            - debugging zorlaşabilir
            - analytics güvenilirliği düşebilir

    Relevance score semantics:
        0.0
            → anlamsal ilişki yok

        0.5
            → orta seviye ilişki

        1.0
            → çok yüksek semantik ilişki

    Örnek kullanım:
        relevance = SemanticRelevance(
            scores_by_question_id={
                "rag_jr_001": 0.91,
                "mlops_mid_002": 0.22,
            }
        )

        score = relevance.get_score("rag_jr_001")

    Bu skor daha sonra scoring engine tarafından:
        - relevance boost
        - retrieval-aware ranking
        - semantic prioritization

    için kullanılabilir.
    """

    scores_by_question_id: dict[str, float] = field(default_factory=dict)
    """
    Question id bazlı semantic relevance skorlarını tutar.

    Key:
        question_id

    Value:
        0.0 - 1.0 arası semantic relevance skoru

    Örnek:
        {
            "rag_jr_001": 0.93,
            "vector_mid_003": 0.81,
            "system_design_002": 0.14,
        }

    Bu skorlar genellikle:
        - embedding similarity
        - vector search
        - reranker output
        - semantic retrieval pipeline

    tarafından üretilir.

    Bu alan neden önemlidir?
        Çünkü scoring engine:
            yalnızca statik rule'lara değil,
            semantic relevance'a da göre karar verebilir.

    Örnek:
        CV embedding'i ile yüksek similarity gösteren sorular:
            daha yüksek suitability score alabilir.

    Kullanım alanları:
        - retrieval-aware scoring
        - semantic ranking
        - relevance boosting
        - adaptive question selection
        - CV-question matching
    """

    def get_score(
        self,
        question_id: str,
    ) -> float:
        """
        Verilen question_id için semantic relevance skorunu döndürür.

        Eğer ilgili question_id relevance map içinde yoksa:
            0.0 döner.

        Neden default 0.0?
            Çünkü relevance bilgisi olmayan soru:
                semantic olarak nötr/düşük relevance

            kabul edilir.

        Bu yaklaşım scoring engine'in:
            - None kontrolü yapmasını önler
            - daha sade scoring logic yazılmasını sağlar
            - defensive davranış üretir

        Örnek:
            relevance.get_score("rag_jr_001")
                -> 0.92

            relevance.get_score("unknown_question")
                -> 0.0

        Bu metod neden helper olarak var?
            Çünkü caller tarafında sürekli:

                scores_by_question_id.get(...)

            yazılmasını önler.

            Ayrıca ileride:
                - normalization
                - logging
                - caching
                - analytics hook

            gibi davranışlar eklemek kolaylaşır.

        Args:
            question_id:
                Semantic relevance skoru alınacak question id.

        Returns:
            float:
                0.0 - 1.0 arası semantic relevance skoru.
        """
        return self.scores_by_question_id.get(question_id, 0.0)