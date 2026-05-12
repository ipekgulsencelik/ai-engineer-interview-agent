from dataclasses import dataclass, field

from src.domain.constants.selection import (
    MIN_SELECTION_SCORE,
)
from src.domain.entities.question import Question
from src.domain.results.selection_breakdown import (
    SelectionBreakdown,
)


@dataclass(frozen=True)
class ScoredCandidate:
    """
    Ranking öncesi skorlanmış candidate state'ini temsil eden immutable
    domain snapshot modelidir.

    Bu modelin temel amacı:
        Scoring aşamasından geçmiş ancak henüz ranking/sorting uygulanmamış
        candidate question state'ini güvenli ve explainable şekilde taşımaktır.

    ----------------------------------------------------------------------
    PIPELINE'DAKİ ROLÜ
    ----------------------------------------------------------------------

    Bu model genellikle selection pipeline'ın şu aşamasında bulunur:

        retrieval
            ↓
        filtering
            ↓
        scoring
            ↓
        ScoredCandidate   ← BU MODEL
            ↓
        ranking
            ↓
        RankedCandidate
            ↓
        selection

    Yani:
        ScoredCandidate ranking öncesi intermediate snapshot'tır.

    ----------------------------------------------------------------------
    NEDEN AYRI MODEL VAR?
    ----------------------------------------------------------------------

    Scoring ve ranking farklı domain aşamalarıdır.

    Scoring aşamasında:
        candidate'lar yalnızca evaluate edilir.

    Ranking aşamasında:
        candidate'lar birbirleriyle karşılaştırılır ve ordering oluşur.

    Bu nedenle:
        "score'u var ama rank'i henüz yok"

    state'ini temsil eden ayrı model gerekir.

    Eğer doğrudan RankedCandidate kullanılırsa:
        henüz sorting yapılmadan fake/geçici rank verilmesi gerekir.

    Bu:
        semantic olarak hatalıdır.

    Bu nedenle:
        ScoredCandidate ve RankedCandidate ayrımı intentional domain design'dır.

    ----------------------------------------------------------------------
    NEDEN RANK YOK?
    ----------------------------------------------------------------------

    Rank:
        candidate'ların birbirleriyle karşılaştırılması sonucu oluşur.

    Örneğin:

        score=9.5 -> rank=1
        score=8.2 -> rank=2

    Rank:
        tek bir candidate'ın intrinsic özelliği değildir.

    Relative ordering sonucudur.

    Bu nedenle:
        scoring aşamasında rank bilgisi bulunmaz.

    Rank yalnızca:
        sorting sonrası oluşur.

    ----------------------------------------------------------------------
    EXPLAINABILITY MİMARİSİ
    ----------------------------------------------------------------------

    Bu model yalnızca final score taşımaz.

    Aynı zamanda:

        SelectionBreakdown

    nesnesini de taşır.

    Böylece:
        final score explainable hale gelir.

    Örneğin:
        - level_score
        - market_score
        - diversity_score
        - fatigue_score

    gibi component'ler korunur.

    Bu yapı:
        - AI transparency
        - debugging
        - analytics
        - auditability
        - recommendation explainability

    açısından kritiktir.

    ----------------------------------------------------------------------
    IMMUTABILITY
    ----------------------------------------------------------------------

    frozen=True intentional tasarım kararıdır.

    Çünkü scoring sonucu:
        immutable snapshot olarak davranmalıdır.

    Örneğin:

        candidate.score = 999

    gibi mutation işlemleri engellenmelidir.

    Bunun avantajları:

        - accidental mutation önlenir
        - deterministic behavior sağlanır
        - debugging kolaylaşır
        - thread safety artar
        - audit consistency korunur

    ----------------------------------------------------------------------
    FIELD METADATA ARCHITECTURE
    ----------------------------------------------------------------------

    Validation kuralları:
        dataclass field metadata üzerinden tanımlanır.

    Örneğin:

        metadata={
            "finite": True,
            "min_value": MIN_SELECTION_SCORE,
        }

    gibi tanımlar validator tarafından runtime'da okunabilir.

    Bu yaklaşımın avantajları:

        - declarative validation sağlar
        - validator generic çalışabilir
        - model self-documenting olur
        - Open/Closed Principle desteklenir
        - field invariant'ları görünür hale gelir

    ----------------------------------------------------------------------
    DOMAIN RESPONSIBILITIES
    ----------------------------------------------------------------------

    Bu model:

        ✔ question taşır
        ✔ final score taşır
        ✔ explainable breakdown taşır
        ✔ immutable snapshot sağlar
        ✔ invariant validation tetikler

    Bu model:

        ✘ scoring hesaplamaz
        ✘ ranking yapmaz
        ✘ sorting yapmaz
        ✘ selection kararı vermez
        ✘ persistence işlemi yapmaz

    ----------------------------------------------------------------------
    DOMAIN CONTRACT
    ----------------------------------------------------------------------

    Bu model şunu temsil eder:

        "Bu question scoring aşamasından geçti ve
        explainable final score üretildi."

    Ancak:
        henüz ranking ordering oluşmamıştır.
    """

    question: Question = field(
        metadata={
            # Candidate'ın temsil ettiği Question domain entity'si.
            #
            # Dict veya primitive veri yerine doğrudan domain entity
            # kullanılması:
            #   - stronger typing sağlar
            #   - richer domain behavior sunar
            #   - domain consistency korur
            #
            # Ranking/scoring pipeline:
            #   category
            #   level
            #   difficulty
            #   keywords
            #
            # gibi alanlara erişebilir.
            "type": Question,
        }
    )

    score: float = field(
        metadata={
            # Score numeric olmalıdır.
            #
            # int ve float kabul edilir.
            #
            # bool değerler validator tarafından ayrıca reddedilebilir.
            "type": (int, float),

            # NaN / infinity / -infinity değerleri reddedilir.
            #
            # Çünkü:
            #   - ranking consistency bozulabilir
            #   - sorting davranışı anlamsız hale gelebilir
            #   - analytics verisi kirlenebilir
            "finite": True,

            # Score negatif olamaz.
            #
            # Selection score semantic olarak:
            #   relevance strength
            #   candidate suitability
            #   ranking contribution
            #
            # anlamı taşır.
            #
            # Bu nedenle minimum boundary uygulanır.
            "min_value": MIN_SELECTION_SCORE,
        }
    )

    breakdown: SelectionBreakdown = field(
        metadata={
            # Explainable scoring breakdown snapshot'ı.
            #
            # Bu alan:
            #   - level_score
            #   - market_score
            #   - diversity_score
            #   - fatigue_score
            #
            # gibi scoring component'lerini taşır.
            #
            # Böylece final score explainable olur.
            #
            # Bu yapı:
            #   - debugging
            #   - AI transparency
            #   - recommendation explainability
            #
            # açısından önemlidir.
            "type": SelectionBreakdown,
        }
    )

    def __post_init__(self) -> None:
        """
        Dataclass initialization tamamlandıktan sonra
        invariant validation çalıştırılır.

        Amaç:
            Invalid ScoredCandidate state'inin
            sistem içine girmesini engellemektir.

        Validation delegation yaklaşımı kullanılır.

        Böylece:
            - model sade kalır
            - validation reusable olur
            - SRP korunur
            - validator bağımsız test edilebilir

        Validation kapsamında örnek kontroller:

            - question doğru domain entity mi?
            - score finite mi?
            - score negatif mi?
            - breakdown geçerli mi?
        """

        from src.domain.validators.scored_candidate_validator import (
            ScoredCandidateValidator,
        )

        ScoredCandidateValidator.validate(self)