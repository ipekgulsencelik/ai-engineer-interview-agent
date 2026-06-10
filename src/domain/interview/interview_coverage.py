from dataclasses import dataclass, field


@dataclass(frozen=True)
class InterviewCoverage:
    """
    Interview sürecinde şimdiye kadar hangi kategori, seviye ve soru tiplerinin
    ne kadar kapsandığını temsil eden immutable coverage snapshot modelidir.

    Bu model interview'in "coverage durumunu" temsil eder.

    Yani sistem şu sorulara cevap verebilir:

        - Hangi kategoriden çok soru soruldu?
        - Hangi kategori hiç sorulmadı?
        - Hangi level fazla temsil edildi?
        - Hangi question type baskın hale geldi?
        - Interview coverage dengeli mi?

    Bu model neden gerekli?
        Eğer interview sistemi yalnızca:
            - market_weight
            - semantic relevance
            - difficulty matching

        gibi sinyallere göre soru seçerse, interview zamanla dengesiz hale
        gelebilir.

    Örnek problem:
        Candidate CV'si sürekli RAG içeriyorsa sistem:

            - sürekli RAG
            - sürekli embedding
            - sürekli retrieval

        soruları seçebilir.

        Bu durumda:
            - interview coverage daralır
            - değerlendirme tek alana sıkışır
            - candidate'ın genel seviyesi ölçülemez

    InterviewCoverage bu problemi çözmeye yardımcı olur.

    Temel amaç:
        Scoring engine'in yalnızca "en alakalı" soruları değil,
        aynı zamanda:

            - dengeli
            - çeşitli
            - adil
            - kapsayıcı

        soru dağılımı üretmesini sağlamaktır.

    Coverage neden scoring için önemlidir?
        İyi bir interview:
            - farklı kategorileri kapsamalı
            - farklı difficulty seviyeleri içermeli
            - farklı question type'ları kullanmalı

        Örneğin:
            - conceptual
            - debugging
            - system design
            - scenario

        soruları dengeli dağıtılabilir.

    Bu model ne yapar?
        - coverage snapshot taşır
        - kategori dağılımını tutar
        - level dağılımını tutar
        - question type dağılımını tutar
        - helper accessor metodları sağlar

    Bu model ne yapmaz?
        - coverage hesaplamaz
        - scoring yapmaz
        - soru seçmez
        - penalty hesaplamaz
        - boost üretmez
        - interview state mutate etmez

    Coverage hesaplama logic'i neden burada değil?
        Çünkü bu model yalnızca immutable snapshot temsil eder.

        Coverage computation logic:
            - ayrı bir service
            - analytics builder
            - coverage tracker

        içinde bulunmalıdır.

    Immutable tasarım:
        frozen=True kullanılmıştır.

        Çünkü coverage scoring sırasında runtime snapshot olarak düşünülür.

        Snapshot mutate edilirse:
            - scoring nondeterministic hale gelebilir
            - debugging zorlaşır
            - test güvenilirliği düşebilir

    Örnek kullanım:
        coverage = InterviewCoverage(
            category_counts={
                "RAG": 4,
                "MLOps": 1,
            },
            question_type_counts={
                "conceptual": 5,
                "debugging": 2,
            },
            total_questions_asked=7,
        )

    Daha sonra scoring engine:

        if coverage.get_category_count("RAG") > 3:
            apply_penalty()

    gibi kararlar verebilir.
    """

    category_counts: dict[str, int] = field(default_factory=dict)
    """
    Her kategoriden kaç soru sorulduğunu tutar.

    Key:
        category adı

    Value:
        o kategoriden sorulan toplam soru sayısı

    Örnek:
        {
            "RAG": 4,
            "MLOps": 1,
            "Vector DB": 2,
        }

    Bu alan neden önemlidir?
        Çünkü interview coverage dengesi category bazında takip edilir.

    Örnek kullanım:
        Eğer "RAG" çok yüksek count'a sahipse:
            yeni RAG sorularına penalty uygulanabilir.

        Eğer "MLOps" hiç sorulmadıysa:
            MLOps sorularına boost uygulanabilir.

    Kullanım alanları:
        - category diversity
        - adaptive balancing
        - coverage-aware scoring
        - interview analytics
    """

    level_counts: dict[str, int] = field(default_factory=dict)
    """
    Her question level için kaç soru sorulduğunu tutar.

    Key:
        level adı

    Value:
        o level'dan sorulan soru sayısı

    Örnek:
        {
            "JR": 3,
            "MID": 5,
            "SENIOR": 1,
        }

    Bu alan neden önemlidir?
        Çünkü interview yalnızca tek difficulty bandında ilerlememelidir.

    Örnek:
        Sürekli SENIOR soru sormak:
            candidate overload yaratabilir.

        Sürekli JR soru sormak:
            candidate'ın gerçek seviyesi ölçülemeyebilir.

    Scoring engine bu alanı kullanarak:
        - level balancing
        - difficulty pacing
        - adaptive progression

    davranışları uygulayabilir.
    """

    question_type_counts: dict[str, int] = field(default_factory=dict)
    """
    Her question type için kaç soru sorulduğunu tutar.

    Örnek question type'lar:
        - conceptual
        - debugging
        - scenario
        - system_design

    Örnek veri:
        {
            "conceptual": 5,
            "debugging": 1,
            "system_design": 0,
        }

    Bu alan neden önemlidir?
        Çünkü iyi bir interview farklı düşünme biçimlerini ölçmelidir.

    Örneğin:
        conceptual:
            teori bilgisi ölçer

        debugging:
            problem çözme becerisi ölçer

        system_design:
            mimari düşünme becerisi ölçer

    Eğer yalnızca conceptual soru sorulursa:
        interview tek boyutlu hale gelir.

    Bu nedenle question type diversity önemlidir.
    """

    total_questions_asked: int = 0
    """
    Interview boyunca toplam kaç soru sorulduğunu temsil eder.

    Bu alan neden gerekli?
        Çünkü bazı scoring kararları toplam interview progression'a göre
        değişebilir.

    Örnek:
        İlk birkaç soruda:
            daha geniş exploration yapılabilir.

        Interview ilerledikçe:
            daha targeted probing yapılabilir.

    Ayrıca coverage ratio hesaplamaları için kullanılabilir.

    Örnek:
        category_ratio =
            category_count / total_questions_asked
    """


    def get_category_count(
        self,
        category: str,
    ) -> int:
        """
        Verilen kategoriden kaç soru sorulduğunu döndürür.

        Eğer kategori coverage içinde yoksa:
            0 döner.

        Neden helper metod kullanılıyor?
            Çünkü caller tarafında sürekli:

                coverage.category_counts.get(...)

            yazılmasını önler.

            Ayrıca ileride:
                - normalization
                - logging
                - analytics hook
                - caching

            gibi davranışlar eklemek kolaylaşır.

        Args:
            category:
                Sorgulanacak kategori adı.

        Returns:
            int:
                O kategoriden sorulan soru sayısı.
        """
        return self.category_counts.get(category, 0)


    def get_level_count(
        self,
        level: str,
    ) -> int:
        """
        Verilen level'dan kaç soru sorulduğunu döndürür.

        Eğer level coverage içinde yoksa:
            0 döner.

        Örnek:
            get_level_count("SENIOR")
                -> 2

        Args:
            level:
                Sorgulanacak question level.

        Returns:
            int:
                İlgili level'dan sorulan soru sayısı.
        """
        return self.level_counts.get(level, 0)


    def get_question_type_count(
        self,
        question_type: str,
    ) -> int:
        """
        Verilen question type'dan kaç soru sorulduğunu döndürür.

        Eğer type coverage içinde yoksa:
            0 döner.

        Örnek:
            get_question_type_count("debugging")
                -> 1

        Bu helper özellikle scoring engine içinde:
            - diversity penalty
            - coverage balancing
            - adaptive selection

        sırasında kullanılabilir.

        Args:
            question_type:
                Sorgulanacak question type adı.

        Returns:
            int:
                İlgili type'dan sorulan soru sayısı.
        """
        return self.question_type_counts.get(question_type, 0)