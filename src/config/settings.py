from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Merkezi application configuration modeli.

    Bu modelin amacı:
        Uygulamanın tüm runtime configuration bilgisini merkezi, type-safe ve
        validate edilmiş şekilde yönetmektir.

    Modern backend sistemlerinde configuration neden önemlidir?
        Çünkü production-grade uygulamalarda:
            - API key'ler
            - model isimleri
            - environment bilgileri
            - database path'leri
            - provider ayarları

        hard-coded tutulmamalıdır.

    Hard-coded configuration problemleri:
        ✘ environment değişimi zorlaşır
        ✘ secret yönetimi riskli olur
        ✘ deployment karmaşıklaşır
        ✘ test isolation zorlaşır
        ✘ CI/CD süreçleri kırılgan olur

    Settings modeli sayesinde:
        ✔ centralized configuration
        ✔ environment-based runtime behavior
        ✔ type-safe config access
        ✔ automatic validation
        ✔ cleaner deployment
        ✔ safer secret handling
        ✔ easier testing

    Neden BaseSettings kullanıyoruz?
        Çünkü pydantic-settings:
            - environment variable parsing
            - type conversion
            - validation
            - .env loading

        gibi kritik özellikleri otomatik sağlar.

    Örnek:
        ENV değişkeni:
            EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

        otomatik olarak:
            str

        tipine dönüştürülür.

    Mimari yaklaşım:
        Settings:
            application configuration boundary

        olarak düşünülmelidir.

    Mimari konum:
        Environment Variables / .env
                    ↓
              Pydantic Settings
                    ↓
                Application

    Bu model hangi alanları yönetiyor?
        ✔ application metadata
        ✔ environment configuration
        ✔ dataset path'leri
        ✔ vector database config
        ✔ embedding model config
        ✔ LLM provider config

    Önemli tasarım notu:
        Settings modeli:
            runtime configuration

        temsil eder.

        Şunları içermez:
            ✘ business logic
            ✘ orchestration
            ✘ provider SDK instance'ları
            ✘ runtime mutable state

    Environment-based architecture neden önemli?
        Çünkü aynı kod:
            - local development
            - staging
            - production
            - CI pipeline

        ortamlarında farklı config ile çalışmalıdır.

    Örnek:
        Development:
            local ChromaDB
            mock evaluator

        Production:
            cloud vector store
            real Groq/OpenAI provider

    Gelecekte eklenebilecek config alanları:
        - OPENAI_API_KEY
        - COHERE_API_KEY
        - LOG_LEVEL
        - TELEMETRY_ENABLED
        - CACHE_TTL
        - RETRY_COUNT
        - RATE_LIMIT
        - REDIS_URL
        - POSTGRES_URL

    Güvenlik notu:
        Secret değerler:
            source control içerisine yazılmamalıdır.

        Bunun yerine:
            .env
            environment variable
            secret manager

        kullanılmalıdır.

    Example:
        settings = Settings()

        print(settings.APP_NAME)

    Output:
        "InterviewForge"
    """

    # ---------------------------------------------------------
    # PYDANTIC SETTINGS CONFIG
    # ---------------------------------------------------------
    # Pydantic Settings'in nasıl davranacağını tanımlar.
    #
    # Bu inner class:
    #   - .env loading
    #   - environment parsing behavior
    #   - case sensitivity
    #   - encoding
    # gibi davranışları kontrol etmek için gereklidir.
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # ---------------------------------------------------------
    # APPLICATION NAME
    # ---------------------------------------------------------
    # Uygulamanın resmi adıdır.
    #
    # Kullanım alanları:
    #   - logging
    #   - telemetry
    #   - API metadata
    #   - CLI headers
    #   - monitoring
    #
    # Örnek:
    #   "InterviewForge"
    #
    # Bu alan zorunludur.
    APP_NAME: str = "AI Engineer Interview Agent"

    # ---------------------------------------------------------
    # ENVIRONMENT NAME
    # ---------------------------------------------------------
    # Uygulamanın hangi environment'ta çalıştığını belirtir.
    #
    # Örnek:
    #   "development"
    #   "staging"
    #   "production"
    #   "test"
    #
    # Varsayılan:
    #   development
    #
    # Bu alan:
    #   - debug behavior
    #   - logging level
    #   - provider selection
    #   - telemetry
    #
    # gibi davranışları etkileyebilir.
    ENV: str = "development"

    # ---------------------------------------------------------
    # QUESTION DATASET PATH
    # ---------------------------------------------------------
    # Interview question dataset dosyasının path bilgisidir.
    #
    # Örnek:
    #   "data/questions.json"
    #
    # JsonQuestionRepository tarafından kullanılır.
    #
    # Bu alan zorunludur.
    QUESTION_DATA_PATH: str = "data/questions.json"

    # ---------------------------------------------------------
    # CHROMA PERSIST DIRECTORY
    # ---------------------------------------------------------
    # ChromaDB vector index verilerinin disk üzerinde tutulacağı dizindir.
    #
    # Örnek:
    #   "data/chroma"
    #
    # ChromaVectorStore tarafından kullanılır.
    CHROMA_PERSIST_DIR: str = "data/chroma"

    # ---------------------------------------------------------
    # CHROMA COLLECTION NAME
    # ---------------------------------------------------------
    # ChromaDB collection adı.
    #
    # Collection:
    #   semantic vector namespace gibi düşünülebilir.
    #
    # Örnek:
    #   "questions"
    #
    # Farklı retrieval dataset'leri için farklı collection'lar kullanılabilir.
    CHROMA_COLLECTION_NAME: str = "questions"

    # ---------------------------------------------------------
    # EMBEDDING MODEL NAME
    # ---------------------------------------------------------
    # Kullanılacak embedding model identifier bilgisidir.
    #
    # Örnek:
    #   "all-MiniLM-L6-v2"
    #   "BAAI/bge-small-en"
    #
    # SentenceTransformerEmbeddingModel tarafından kullanılır.
    #
    # Bu config sayesinde:
    #   embedding backend değiştirmek kolaylaşır.
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # ---------------------------------------------------------
    # GROQ API KEY
    # ---------------------------------------------------------
    # Groq provider authentication secret bilgisidir.
    #
    # Varsayılan:
    #   ""
    #
    # Production ortamında environment variable üzerinden verilmelidir.
    #
    # Güvenlik notu:
    #   API key source control'e yazılmamalıdır.
    #
    # Kullanım alanları:
    #   - Groq evaluator
    #   - LLM inference
    #   - interview evaluation
    GROQ_API_KEY: str = ""

    # ---------------------------------------------------------
    # GROQ MODEL NAME
    # ---------------------------------------------------------
    # Kullanılacak Groq model identifier bilgisidir.
    #
    # Örnek:
    #   "llama3-70b-8192"
    #   "mixtral-8x7b-32768"
    #
    # Bu config sayesinde:
    #   model switching centralized hale gelir.
    GROQ_MODEL_NAME: str = "llama3-70b-8192"


# ---------------------------------------------------------
# GLOBAL SETTINGS INSTANCE
# ---------------------------------------------------------
# Uygulama genelinde kullanılacak merkezi Settings instance'ı oluşturulur.
#
# Böylece:
#   from src.config.settings import settings
#
# şeklinde centralized config access sağlanır.
#
# Bu instance:
#   import sırasında environment variable'ları parse eder.
settings = Settings()
