from __future__ import annotations

from dataclasses import dataclass

from src.domain.interview.adaptive_pacing import AdaptivePacing
from src.domain.interview.interview_coverage import (
    InterviewCoverage,
)
from src.domain.interview.question_fatigue import (
    QuestionFatigue,
)
from src.domain.retrieval.semantic_relevance import (
    SemanticRelevance,
)
from src.domain.scoring.scoring_weights import ScoringWeights
from src.domain.validators.scoring_signals_validator import (
    ScoringSignalsValidator,
)


@dataclass(frozen=True)
class ScoringSignals:
    """
    Scoring engine tarafından kullanılan gelişmiş runtime sinyallerini taşıyan
    immutable domain support modelidir.

    Bu model, temel ScoringContext bilgisinden ayrı tutulmuştur.

    ScoringContext daha temel interview state bilgisini taşır:

        - current_level
        - cv_skills
        - asked_question_ids
        - recent_scores
        - weak_areas

    ScoringSignals ise daha gelişmiş, opsiyonel ve genişletilebilir scoring
    sinyallerini temsil eder:

        - interview coverage
        - question fatigue
        - semantic relevance
        - adaptive pacing
        - custom weights

    Neden ScoringContext içine eklenmedi?
        Çünkü ScoringContext temel context snapshot'ıdır.

        Eğer tüm gelişmiş sinyaller doğrudan ScoringContext içine eklenirse:
            - context modeli şişer
            - temel scoring ile advanced scoring birbirine karışır
            - test setup karmaşıklaşır
            - her scoring algoritması ihtiyaç duymadığı alanları da taşımak
              zorunda kalır

    Bu ayrımın avantajları:
        - core context sade kalır
        - advanced sinyaller izole edilir
        - sinyal bazlı test yazmak kolaylaşır
        - yeni scoring sinyali eklemek daha güvenli olur
        - scoring algoritmaları modüler şekilde genişletilebilir

    Bu model ne yapar?
        - Gelişmiş scoring sinyallerini taşır.
        - Optional signal kullanımına izin verir.
        - Custom ağırlık değerlerini merkezi olarak saklar.
        - Oluşturulduktan sonra validator çalıştırır.

    Bu model ne yapmaz?
        - skor hesaplamaz
        - soru seçmez
        - coverage hesaplamaz
        - fatigue hesaplamaz
        - semantic retrieval çalıştırmaz
        - adaptive pacing üretmez
        - persistence işlemi yapmaz

    Immutable tasarım:
        frozen=True kullanılmıştır.

        Çünkü scoring sırasında kullanılan sinyaller runtime snapshot olarak
        düşünülmelidir.

        Scoring engine bu sinyalleri mutate etmemelidir.

        Böylece:
            - side-effect riski azalır
            - scoring deterministic kalır
            - test edilebilirlik artar
            - debugging kolaylaşır
    """

    coverage: InterviewCoverage | None = None
    """
    Interview boyunca kategori/konu kapsama durumunu temsil eden coverage
    sinyalidir.

    Bu sinyal, interview'in belirli alanlara fazla veya az odaklanıp
    odaklanmadığını analiz etmek için kullanılabilir.

    Örnek kullanım:
        Eğer "RAG" kategorisinden çok fazla soru sorulduysa,
        scoring engine yeni RAG sorularına penalty uygulayabilir.

        Eğer "System Design" henüz hiç sorulmadıysa,
        bu kategoriye ait sorular boost alabilir.

    Amaç:
        - category diversity sağlamak
        - interview coverage dengesini korumak
        - tek konuya aşırı yığılmayı önlemek
        - değerlendirme kapsamını genişletmek
    """

    fatigue: QuestionFatigue | None = None
    """
    Adayın cognitive fatigue / question fatigue durumunu temsil eden sinyaldir.

    Bu sinyal, üst üste zor, uzun veya aynı tipte sorular sorulup
    sorulmadığını değerlendirmek için kullanılabilir.

    Örnek:
        Son 3 soru çok zor veya system design ağırlıklıysa,
        scoring engine daha hafif veya farklı tipte bir soruyu öne çıkarabilir.

    Amaç:
        - adayın bilişsel yükünü dengelemek
        - interview pacing'i iyileştirmek
        - üst üste aşırı zor soru sormaktan kaçınmak
        - daha doğal ve sürdürülebilir mülakat akışı sağlamak
    """

    semantic_relevance: SemanticRelevance | None = None
    """
    Retrieval veya embedding tabanlı semantic relevance bilgisini temsil eder.

    Bu sinyal, bir sorunun mevcut interview amacı, CV içeriği veya önceki
    cevaplarla semantik olarak ne kadar ilişkili olduğunu gösterebilir.

    Örnek:
        Candidate CV'sinde "vector database" ağırlıklıysa,
        vector search veya embedding sorularının semantic relevance skoru
        daha yüksek olabilir.

    Kullanım alanları:
        - retrieval-aware question selection
        - semantic similarity scoring
        - CV ile question matching
        - topic relevance boost
        - semantic duplicate suppression
    """

    adaptive_pacing: AdaptivePacing | None = None
    """
    Interview akışının aday performansına göre hızını ve zorluk geçişlerini
    ayarlamak için kullanılan adaptive pacing sinyalidir.

    Bu sinyal, sistemin adaya ne zaman daha zor, daha kolay veya daha dengeli
    soru sorması gerektiğini belirlemesine yardımcı olabilir.

    Örnek:
        Aday son sorularda çok yüksek skor aldıysa:
            daha zor soru seçilebilir.

        Aday son sorularda düşük skor aldıysa:
            daha temel veya destekleyici soru seçilebilir.

    Amaç:
        - difficulty progression yönetmek
        - candidate overload riskini azaltmak
        - adaptive interview deneyimi üretmek
        - performansa göre soru seçimini dinamikleştirmek
    """

    weights: ScoringWeights | None = None
    """
    Scoring algoritmalarında kullanılacak custom ağırlık değerlerini taşıyan sinyaldir.

    Bu sinyal, farklı scoring sinyallerine atanacak önem derecesini dinamik olarak ayarlamak için kullanılabilir.
    
    Örnek:
        Eğer interview'in başındaysak ve coverage sinyaline güveniyorsak:
            weights = ScoringWeights(coverage_weight=1.5)
        Eğer interview'in ilerleyen aşamalarındaysak ve fatigue sinyaline daha fazla önem vermek istiyorsak:
            weights = ScoringWeights(fatigue_weight=1.2)
    
    Amaç:
        - scoring sinyallerinin önemini dinamik olarak ayarlamak
        - farklı interview aşamalarında farklı sinyallere odaklanmak
        - scoring algoritmalarını daha esnek hale getirmek

    Not:
        Bu sinyal sadece ağırlık değerlerini taşır, kendisi skor hesaplamaz.
        Scoring engine, bu ağırlıkları diğer sinyallerle birlikte kullanarak nihai skorları hesaplar.   
    """

    def __post_init__(self) -> None:
        """
        Dataclass oluşturulduktan sonra ScoringSignals validation kurallarını
        çalıştırır.

        Bu metodun amacı:
            - optional sinyal tiplerinin doğru olup olmadığını kontrol etmek
            - custom_weights yapısının geçerli olup olmadığını doğrulamak
            - runtime signal snapshot'ının domain açısından güvenli kalmasını
              sağlamaktır

        Validation neden burada?
            ScoringSignals nesnesi oluşturulduğu anda geçerli olmalıdır.

            Böylece scoring engine:
                "bu sinyaller geçerli mi?"

            sorusunu tekrar tekrar kontrol etmek zorunda kalmaz.

        Raises:
            ValueError:
                ScoringSignals alanlarından biri domain kurallarını ihlal
                ederse fırlatılır.
        """
        ScoringSignalsValidator.validate(self)