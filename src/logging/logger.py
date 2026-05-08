import logging
import sys

import structlog


def configure_logging() -> None:
    """
    Merkezi structured logging configuration'ını initialize eder.

    Bu fonksiyonun amacı:
        Uygulama genelindeki logging davranışını merkezi, tutarlı ve
        production-friendly şekilde yapılandırmaktır.

    Structured logging nedir?
        Structured logging:
            log'ların yalnızca düz text yerine yapılandırılmış veri
            formatında üretilmesidir.

    Geleneksel log:
        "User login failed."

    Structured log:
        {
            "event": "user_login_failed",
            "user_id": 123,
            "timestamp": "...",
            "level": "error"
        }

    Structured logging neden önemli?
        Çünkü modern production sistemlerinde log'lar:
            - machine-readable
            - searchable
            - filterable
            - aggregatable

        olmalıdır.

    Özellikle:
        - distributed systems
        - AI pipelines
        - observability platforms
        - telemetry systems
        - cloud-native applications

        için kritik öneme sahiptir.

    Bu configuration ne sağlar?
        ✔ JSON log output
        ✔ timestamp enrichment
        ✔ log level metadata
        ✔ centralized logging setup
        ✔ stdout streaming
        ✔ structured telemetry readiness

    Bu yapı neden structlog kullanıyor?
        Çünkü structlog:
            - structured logging odaklıdır
            - modern Python logging yaklaşımıdır
            - JSON logging'i kolaylaştırır
            - context binding destekler
            - observability sistemleriyle uyumludur

    Logging neden merkezi configure edilmeli?
        Çünkü dağınık logging setup:
            - inconsistent log format
            - observability problemleri
            - parsing zorlukları
            - debugging karmaşası

        oluşturabilir.

    Merkezi configuration sayesinde:
        ✔ consistent log format
        ✔ centralized control
        ✔ easier maintenance
        ✔ production readiness

    Bu setup hangi ortamlar için uygundur?
        ✔ local development
        ✔ Docker containers
        ✔ Kubernetes
        ✔ CI/CD pipelines
        ✔ cloud logging systems

    stdout neden kullanılıyor?
        Çünkü modern containerized sistemlerde:
            stdout/stderr logging standard yaklaşımdır.

        Özellikle:
            - Docker
            - Kubernetes
            - ECS
            - Cloud Run

        log collector'ları stdout'u otomatik toplar.

    Gelecekte eklenebilecek geliştirmeler:
        - request_id binding
        - trace_id correlation
        - OpenTelemetry integration
        - environment-aware log levels
        - async logging
        - file rotation
        - Sentry integration
        - redaction processors
        - contextual metadata
        - performance telemetry

    Mimari not:
        Logging:
            cross-cutting concern

        olarak değerlendirilir.

        Bu yüzden:
            centralized infrastructure setup

        şeklinde organize edilmesi doğrudur.
    """

    # ---------------------------------------------------------
    # STANDARD LIBRARY LOGGING CONFIGURATION
    # ---------------------------------------------------------
    # Python standard logging sistemi initialize edilir.
    #
    # format="%(message)s":
    #   Structlog zaten structured JSON üreteceği için ek metadata burada
    #   tekrar eklenmez.
    #
    # stream=sys.stdout:
    #   Log output stdout'a yönlendirilir.
    #
    # level=logging.INFO:
    #   INFO ve üzeri seviyeler aktif edilir.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # ---------------------------------------------------------
    # STRUCTLOG CONFIGURATION
    # ---------------------------------------------------------
    # structlog pipeline configuration yapılır.
    #
    # Structlog:
    #   logging event'lerini processor pipeline üzerinden geçirerek
    #   structured output üretir.
    structlog.configure(
        # ---------------------------------------------------------
        # PROCESSOR PIPELINE
        # ---------------------------------------------------------
        # Her log event'i sırasıyla bu processor'lardan geçer.
        processors=[
            # ---------------------------------------------------------
            # TIMESTAMP PROCESSOR
            # ---------------------------------------------------------
            # Her log event'ine ISO format timestamp ekler.
            #
            # Örnek:
            #   "timestamp": "2026-05-08T12:00:00Z"
            #
            # Bu:
            #   - observability
            #   - tracing
            #   - debugging
            #
            # için kritik öneme sahiptir.
            structlog.processors.TimeStamper(
                fmt="iso",
            ),
            # ---------------------------------------------------------
            # LOG LEVEL PROCESSOR
            # ---------------------------------------------------------
            # Log severity level bilgisini event'e ekler.
            #
            # Örnek:
            #   "level": "info"
            #
            # Bu:
            #   - filtering
            #   - monitoring
            #   - alerting
            #
            # için kullanılır.
            structlog.processors.add_log_level,
            # ---------------------------------------------------------
            # JSON RENDERER
            # ---------------------------------------------------------
            # Final log event'ini JSON string'e dönüştürür.
            #
            # Böylece log'lar:
            #   - machine-readable
            #   - structured
            #   - parseable
            #
            # hale gelir.
            #
            # Örnek çıktı:
            # {
            #   "event": "evaluation_completed",
            #   "score": 8.5,
            #   "level": "info"
            # }
            structlog.processors.JSONRenderer(),
        ],
        # ---------------------------------------------------------
        # FILTERING BOUND LOGGER
        # ---------------------------------------------------------
        # Minimum aktif log seviyesini belirler.
        #
        # INFO ve üzeri log'lar işlenecektir.
        #
        # DEBUG log'lar filtrelenir.
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        # ---------------------------------------------------------
        # LOGGER FACTORY
        # ---------------------------------------------------------
        # Structlog logger instance üretim stratejisini belirler.
        #
        # PrintLoggerFactory:
        #   stdout tabanlı basit logger üretir.
        #
        # Containerized sistemler için uygundur.
        logger_factory=structlog.PrintLoggerFactory(),
        # ---------------------------------------------------------
        # LOGGER CACHE
        # ---------------------------------------------------------
        # İlk kullanım sonrası logger instance cache edilir.
        #
        # Avantaj:
        #   repeated logger creation maliyetini azaltır.
        cache_logger_on_first_use=True,
    )


# ---------------------------------------------------------
# GLOBAL LOGGER INSTANCE
# ---------------------------------------------------------
# Application-wide reusable structured logger instance.
#
# Kullanım:
#   logger.info(
#       "evaluation_completed",
#       score=8.5,
#       question_id="rag_001",
#   )
#
# Örnek çıktı:
# {
#   "event": "evaluation_completed",
#   "score": 8.5,
#   "question_id": "rag_001",
#   "level": "info",
#   "timestamp": "..."
# }
logger = structlog.get_logger()
