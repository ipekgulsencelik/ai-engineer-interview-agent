from enum import StrEnum


class QuestionCategory(StrEnum):
    """
    Interview sisteminde desteklenen soru kategorilerini temsil eden enum
    modelidir.

    Bu enum interview sırasında kullanılabilecek farklı question category'lerini
    standartlaştırır.

    Amaç:
        Sistemde question category kullanımını güvenli, tutarlı ve type-safe hale
        getirmektir.

    Neden question category önemli?
        Çünkü iyi bir teknik interview yalnızca tek tip soru sormamalıdır.

        Farklı question category'ler adayın farklı yetkinliklerini ölçer.

    Örnek:
        algorithms:
            algoritma tasarımı ve analizi becerisi ölçer
        system_design:
            büyük ölçekli sistem tasarımı becerisi ölçer
        coding:
            kodlama ve implementation becerisi ölçer
        debugging:
            hata ayıklama ve problem çözme becerisi ölçer
        behavioral:
            iletişim, takım çalışması ve kültüfit uyum becerisi ölçer
        scenario:
            gerçek dünya mühendislik senaryolarında karar verme becerisi ölçer
    Eğer sistem sadece tek tip soru sorarsa:
        - interview monotonlaşır
        - skill coverage düşer
        - adayın bazı güçlü yönleri hiç ölçülemez
        - gerçek mühendislik yetkinliği tam değerlendirilemez
    Bu enum sayesinde sistem:
        ✔ balanced interview flow oluşturabilir
        ✔ question diversity sağlayabilir
        ✔ coverage tracking yapabilir
        ✔ type-aware scoring uygulayabilir
        ✔ adaptive interview strategy geliştirebilir
    Neden Enum kullanıyoruz?
        Çünkü raw string kullanımı:
            - hataya açık olabilir
            - tutarsızlık yaratabilir
            - type-safe değildir
        Enum kullanımı:
            - typo riskini ortadan kaldırır
            - tutarlı naming sağlar
            - type safety sunar
    Problem örnekleri:
        "algo"
        "algorithm"
        "system design"
        "system-design"
        "behavioral"
        "behavior"
        gibi tutarsız değerler sistem davranışını bozabilir.
    Enum kullanmanın avantajları:
        ✔ Type safety
        ✔ IDE autocomplete
        ✔ merkezi validation
        ✔ daha okunabilir API
        ✔ safer refactor
        ✔ domain odaklı modeling
    """
    
    ALGORITHMS = "algorithms"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    DEBUGGING = "debugging"
    BEHAVIORAL = "behavioral"
    SCENARIO = "scenario"   
    LLM_FUNDAMENTALS = "llm_fundamentals"
    PROMPT_ENGINEERING = "prompt_engineering"
    RAG = "rag"
    VECTOR_DB_AND_EMBEDDING = "vector_db_and_embedding"
    AGENTS = "agents"
    EVALUATION = "evaluation"
    MLOPS = "mlops"
    FINE_TUNING = "fine_tuning"