HIGH_SIMILARITY_PENALTY = 0.60
MODERATE_SIMILARITY_PENALTY = 0.85
DEFAULT_DIVERSITY_SCORE = 1.0

MODERATE_SIMILARITY_THRESHOLD = 0.70
DEFAULT_DUPLICATE_THRESHOLD = 0.85


def compute_semantic_diversity_score(
    max_similarity_to_asked: float | None,
    duplicate_threshold: float = DEFAULT_DUPLICATE_THRESHOLD,
) -> float:
    """
    Semantic diversity skorunu hesaplar.

    Amaç:
        Daha önce sorulmuş sorularla semantic olarak aşırı benzer
        candidate question'ları penalize ederek interview çeşitliliğini
        korumaktır.

    Bu scoring rule:
        semantic duplicate prevention

    mekanizması olarak çalışır.

    Problem:
        Sadece keyword-based diversity kontrolü yeterli değildir.

        Örnek:
            "What is RAG?"
            "Explain Retrieval-Augmented Generation."

        keyword olarak farklı görünse de semantic olarak neredeyse aynıdır.

    Bu yüzden:
        embedding similarity

    tabanlı duplicate detection gerekir.

    Semantic diversity neden önemli?
        Çünkü interview sırasında:
            - aynı kavramın tekrar tekrar sorulması
            - benzer reasoning pattern'lerinin dönmesi
            - candidate fatigue oluşması
            - coverage düşmesi

        interview kalitesini azaltır.

    Bu scoring rule sayesinde:
        ✔ semantic tekrar azalır
        ✔ interview coverage artar
        ✔ candidate fatigue azalır
        ✔ daha doğal interview flow oluşur
        ✔ adaptive interview quality yükselir

    Args:
        max_similarity_to_asked:
            Candidate question'ın daha önce sorulan sorularla olan
            en yüksek semantic similarity skoru.

            Beklenen aralık:
                0.0 - 1.0

            Örnek:
                0.92 → çok yüksek similarity
                0.75 → orta similarity
                0.30 → düşük similarity

        duplicate_threshold:
            Semantic duplicate risk eşiği.

            Bu threshold üzerindeki similarity değerleri:
                "semantic duplicate"

            olarak değerlendirilir.

            Varsayılan:
                0.85

    Returns:
        float:
            Diversity multiplier skoru.

            1.0:
                semantic olarak yeterince farklı

            0.85:
                orta düzey semantic benzerlik

            0.60:
                yüksek duplicate riski

    Design Principles:
        ✔ Single Responsibility Principle
            Method yalnızca semantic diversity scoring yapar.

        ✔ Open/Closed Principle
            Threshold ve penalty constant'ları dışarıdan genişletilebilir.

        ✔ Magic Number Elimination
            Tüm kritik skorlar named constant olarak tanımlanmıştır.

        ✔ Readability
            Intent-revealing constant isimleri kullanılmıştır.

        ✔ Maintainability
            Penalty tuning merkezi hale getirilmiştir.

    Gelecekte geliştirilebilecek alanlar:
        - dynamic thresholding
        - category-aware diversity
        - recency-aware duplicate scoring
        - nonlinear penalty curves
        - adaptive diversity tuning
        - embedding confidence weighting
    """

    # ---------------------------------------------------------
    # NO SEMANTIC INFORMATION
    # ---------------------------------------------------------
    # Semantic similarity bilgisi yoksa:
    #   diversity penalize uygulanmaz.
    #
    # Çünkü sistem duplicate riski hakkında yeterli bilgiye sahip değildir.
    if max_similarity_to_asked is None:
        return DEFAULT_DIVERSITY_SCORE

    # ---------------------------------------------------------
    # HIGH DUPLICATE RISK
    # ---------------------------------------------------------
    # Çok yüksek semantic similarity:
    #   interview diversity için ciddi risktir.
    #
    # Örnek:
    #   "What is RAG?"
    #   "Explain Retrieval-Augmented Generation."
    #
    # Bu durumda güçlü penalize uygulanır.
    if max_similarity_to_asked >= duplicate_threshold:
        return HIGH_SIMILARITY_PENALTY

    # ---------------------------------------------------------
    # MODERATE SIMILARITY
    # ---------------------------------------------------------
    # Semantic olarak belirli seviyede benzerlik vardır.
    #
    # Ancak tamamen duplicate değildir.
    #
    # Bu yüzden hafif penalize uygulanır.
    if max_similarity_to_asked >= MODERATE_SIMILARITY_THRESHOLD:
        return MODERATE_SIMILARITY_PENALTY

    # ---------------------------------------------------------
    # HEALTHY SEMANTIC DIVERSITY
    # ---------------------------------------------------------
    # Candidate question semantic olarak yeterince farklıdır.
    #
    # Diversity açısından risk oluşturmaz.
    return DEFAULT_DIVERSITY_SCORE
