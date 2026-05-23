from __future__ import annotations

from abc import ABC, abstractmethod

from src.application.models.llm_request import (
    LLMRequest,
)
from src.application.models.llm_response import (
    LLMResponse,
)


class LLMClient(ABC):
    """
    Provider-independent text generation application port.

    Bu port:
        - application katmanını provider implementasyonlarından izole eder
        - OpenAI, Groq, Anthropic veya local model adapter'larını soyutlar
        - unified request/response contract sağlar

    Concrete implementasyonlar infrastructure katmanında yer almalıdır.
    """

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Provider-independent text generation işlemi gerçekleştirir.

        Args:
            request:
                Generation configuration ve prompt bilgilerini taşıyan
                provider-agnostic request modeli.

        Returns:
            LLMResponse:
                Normalize edilmiş provider-independent generation sonucu.
        """
        ...