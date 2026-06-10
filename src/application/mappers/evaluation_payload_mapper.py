from __future__ import annotations

from typing import Any

from src.application.extractors.payload_field_extractor import (
    PayloadFieldExtractor,
)
from src.application.models.evaluation_payload import (
    EvaluationPayload,
)


class EvaluationPayloadMapper:
    """
    Raw evaluator dict payload'ını EvaluationPayload application schema modeline çevirir.

    Bu sınıf:
        - JSON parse etmez
        - LLMResponse bilmez
        - EvaluationResult üretmez
        - business fallback uygulamaz
    """

    @classmethod
    def from_dict(
        cls,
        payload: dict[str, Any],
    ) -> EvaluationPayload:
        if not isinstance(payload, dict):
            raise TypeError(
                "payload must be a dictionary."
            )

        return EvaluationPayload(
            score=PayloadFieldExtractor.get_optional_float(
                payload,
                "score",
            ),
            feedback=PayloadFieldExtractor.get_optional_string(
                payload,
                "feedback",
            ),
            technical_accuracy=PayloadFieldExtractor.get_optional_float(
                payload,
                "technical_accuracy",
            ),
            depth=PayloadFieldExtractor.get_optional_float(
                payload,
                "depth",
            ),
            communication=PayloadFieldExtractor.get_optional_float(
                payload,
                "communication",
            ),
            missing_keywords=PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "missing_keywords",
            ),
            follow_up_question=PayloadFieldExtractor.get_optional_string(
                payload,
                "follow_up_question",
            ),
            confidence=PayloadFieldExtractor.get_optional_float(
                payload,
                "confidence",
            ),
            rubric_version=PayloadFieldExtractor.get_optional_string(
                payload,
                "rubric_version",
            ),
        )