from __future__ import annotations

from src.application.factories.evaluation_result_factory import (
    EvaluationResultFactory,
)
from src.application.mappers.evaluation_payload_mapper import (
    EvaluationPayloadMapper,
)
from src.application.models.llm_response import (
    LLMResponse,
)
from src.application.parsers.json_response_parser import (
    JsonResponseParser,
)
from src.application.validators.evaluator_response_validator import (
    EvaluatorResponseValidator,
)
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class EvaluatorResponseParser:
    """
    Raw evaluator response orchestration layer.

    Pipeline:
        LLMResponse
            -> raw JSON dict
            -> EvaluationPayload
            -> EvaluationResult
    """

    @classmethod
    def parse(
        cls,
        response: LLMResponse,
    ) -> EvaluationResult:
        EvaluatorResponseValidator.validate(
            response,
        )

        raw_payload = JsonResponseParser.parse_object(
            response.text,
        )

        evaluation_payload = EvaluationPayloadMapper.from_dict(
            raw_payload,
        )

        return EvaluationResultFactory.create(
            evaluation_payload,
        )