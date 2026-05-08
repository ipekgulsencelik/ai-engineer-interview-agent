from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    """
    LLM provider yapılandırmasını temsil eden immutable configuration model.

    Bu model:
        Groq, OpenAI, Anthropic, Ollama veya local inference provider'ları
        gibi farklı LLM backend'lerinin ortak çalışma ayarlarını merkezi
        şekilde temsil eder.

    Amaç:
        Provider configuration bilgisini:
            - type-safe
            - immutable
            - validate edilmiş
            - reusable

        bir yapı altında toplamak.

    Neden ayrı config modeli kullanıyoruz?
        Çünkü production-grade AI sistemlerinde provider ayarları:
            - application logic'ten ayrılmalıdır
            - merkezi yönetilmelidir
            - validation içermelidir
            - kolay değiştirilebilir olmalıdır

    Eğer config dağınık tutulursa:
        - hard-coded değerler oluşur
        - provider migration zorlaşır
        - inconsistent configuration oluşur
        - debugging zorlaşır
        - test setup karmaşık hale gelir

    ProviderConfig sayesinde:
        ✔ centralized configuration
        ✔ immutable runtime config
        ✔ safer provider switching
        ✔ configuration validation
        ✔ cleaner dependency injection
        ✔ testability
        ✔ reproducible inference behavior

    Bu model hangi provider'lar için kullanılabilir?
        - Groq
        - OpenAI
        - Anthropic
        - Ollama
        - LM Studio
        - Azure OpenAI
        - local vLLM
        - HuggingFace inference endpoint

    Neden frozen=True?
        Çünkü runtime sırasında provider configuration'ın değişmesi
        genellikle risklidir.

        Mutable config:
            - nondeterministic behavior
            - debugging zorluğu
            - inconsistent inference
            - concurrency problemleri

        oluşturabilir.

        Immutable config sayesinde:
            - provider behavior stabil kalır
            - reproducibility korunur
            - orchestration daha güvenilir olur

    Bu model hangi ayarları içeriyor?
        provider_name:
            Kullanılan provider adı.

        model_name:
            Kullanılan model identifier.

        temperature:
            Sampling randomness seviyesi.

        max_tokens:
            Maksimum output token limiti.

        timeout_seconds:
            Provider request timeout süresi.

    Kullanım alanları:
        - LLMClient implementations
        - Evaluator setup
        - dependency injection
        - provider factory
        - inference orchestration
        - telemetry
        - testing
        - benchmarking

    Önemli tasarım notu:
        Bu model:
            configuration state

        temsil eder.

        Şunları içermez:
            ✘ API key
            ✘ authentication logic
            ✘ retry strategy
            ✘ provider SDK objects
            ✘ request payloads

        Çünkü bunlar:
            infrastructure concern'dür.

    Güvenlik notu:
        API key gibi secret bilgiler bilinçli olarak bu model içerisinde
        tutulmamaktadır.

        Çünkü:
            - accidental logging
            - serialization leakage
            - debugging exposure

        riskleri oluşturabilir.

    Gelecekte eklenebilecek alanlar:
        - top_p
        - frequency_penalty
        - presence_penalty
        - seed
        - retry_count
        - streaming_enabled
        - base_url
        - rate_limit_config
        - batching_config

    Example:
        config = ProviderConfig(
            provider_name="groq",
            model_name="llama3-70b-8192",
            temperature=0.2,
            max_tokens=1024,
        )

        print(config.model_name)

    Output:
        "llama3-70b-8192"
    """

    # ---------------------------------------------------------
    # PROVIDER NAME
    # ---------------------------------------------------------
    # Kullanılan inference provider'ın adını temsil eder.
    #
    # Örnek:
    #   "groq"
    #   "openai"
    #   "anthropic"
    #   "ollama"
    #
    # Bu alan:
    #   - provider routing
    #   - telemetry
    #   - analytics
    #   - factory resolution
    #
    # için kullanılabilir.
    provider_name: str

    # ---------------------------------------------------------
    # MODEL NAME
    # ---------------------------------------------------------
    # Kullanılan model identifier bilgisidir.
    #
    # Örnek:
    #   "llama3-70b-8192"
    #   "gpt-4o"
    #   "claude-3-opus"
    #
    # Bu alan:
    #   - provider request creation
    #   - benchmarking
    #   - telemetry
    #
    # için kritik öneme sahiptir.
    model_name: str

    # ---------------------------------------------------------
    # TEMPERATURE
    # ---------------------------------------------------------
    # Sampling randomness seviyesini kontrol eder.
    #
    # Düşük temperature:
    #   - daha deterministic output
    #   - daha stabil reasoning
    #
    # Yüksek temperature:
    #   - daha yaratıcı output
    #   - daha fazla varyasyon
    #
    # Evaluation sistemlerinde genellikle düşük temperature tercih edilir.
    #
    # Varsayılan:
    #   0.2
    #
    # Çünkü interview evaluation:
    #   mümkün olduğunca tutarlı olmalıdır.
    temperature: float = 0.2

    # ---------------------------------------------------------
    # MAX TOKENS
    # ---------------------------------------------------------
    # Provider'ın üretebileceği maksimum output token sayısı.
    #
    # Amaç:
    #   - runaway generation önlemek
    #   - maliyet kontrolü
    #   - latency kontrolü
    #   - predictable inference behavior
    #
    # Varsayılan:
    #   1024
    #
    # Faz-1 interview evaluation için yeterlidir.
    max_tokens: int = 1024

    # ---------------------------------------------------------
    # TIMEOUT SECONDS
    # ---------------------------------------------------------
    # Provider request timeout süresi.
    #
    # Amaç:
    #   Sonsuz bekleme durumlarını önlemek.
    #
    # Özellikle:
    #   - network problemleri
    #   - provider latency spike
    #   - inference stall
    #
    # durumlarında kritik öneme sahiptir.
    #
    # Varsayılan:
    #   30 saniye
    timeout_seconds: int = 30

    def __post_init__(self) -> None:
        """
        ProviderConfig oluşturulduktan sonra domain validation kurallarını
        çalıştırır.

        Amaç:
            Geçersiz provider configuration state'lerinin sistem içerisine
            girmesini engellemek.

        Doğrulanan kurallar:
            - provider_name boş olamaz
            - model_name boş olamaz
            - temperature 0-2 arasında olmalı
            - max_tokens > 0 olmalı
            - timeout_seconds > 0 olmalı

        Neden validation önemli?
            Çünkü invalid config:
                - runtime inference failure
                - provider API errors
                - unstable orchestration
                - nondeterministic behavior

            oluşturabilir.

        Design Note:
            Validation domain model seviyesinde yapılır.

            Böylece:
                - invalid state erken yakalanır
                - provider implementation sade kalır
                - centralized validation sağlanır
        """

        # ---------------------------------------------------------
        # PROVIDER NAME VALIDATION
        # ---------------------------------------------------------
        # Provider adı boş olamaz.
        #
        # Çünkü provider routing için zorunludur.
        #
        # strip():
        #   yalnızca whitespace içeren string'leri de engeller.
        if not self.provider_name.strip():
            raise ValueError("Provider name cannot be empty.")

        # ---------------------------------------------------------
        # MODEL NAME VALIDATION
        # ---------------------------------------------------------
        # Model identifier boş olamaz.
        #
        # Çünkü inference request oluşturmak için gereklidir.
        #
        # Örnek geçerli değerler:
        #   "gpt-4o"
        #   "llama3-70b-8192"
        if not self.model_name.strip():
            raise ValueError("Model name cannot be empty.")

        # ---------------------------------------------------------
        # TEMPERATURE VALIDATION
        # ---------------------------------------------------------
        # Temperature yalnızca:
        #   0 <= temperature <= 2
        #
        # aralığında olmalıdır.
        #
        # Çoğu provider bu aralığı kullanır.
        #
        # Invalid değerler:
        #   - unstable sampling
        #   - provider rejection
        #
        # oluşturabilir.
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2.")

        # ---------------------------------------------------------
        # MAX TOKENS VALIDATION
        # ---------------------------------------------------------
        # max_tokens pozitif olmalıdır.
        #
        # 0 veya negatif token limiti anlamsızdır.
        if self.max_tokens <= 0:
            raise ValueError("Max tokens must be greater than 0.")

        # ---------------------------------------------------------
        # TIMEOUT VALIDATION
        # ---------------------------------------------------------
        # Timeout süresi pozitif olmalıdır.
        #
        # 0 veya negatif timeout:
        #   invalid request lifecycle oluşturur.
        if self.timeout_seconds <= 0:
            raise ValueError("Timeout seconds must be greater than 0.")
