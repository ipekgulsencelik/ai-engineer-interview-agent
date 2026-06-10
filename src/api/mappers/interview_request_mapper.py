from __future__ import annotations

from src.api.schemas.interview.requests import (
    InterviewStepRequest,
)
from src.application.use_cases.run_interview_step_use_case import (
    RunInterviewStepPayload,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class RunInterviewStepPayloadMapper:
    """
    Maps InterviewStepRequest into RunInterviewStepPayload.
    """

    @staticmethod
    def to_payload(
        *,
        request: InterviewStepRequest,
    ) -> RunInterviewStepPayload:
        """
        Convert API request DTO into application use-case payload.
        """

        return RunInterviewStepPayload(
            query=request.query,
            answer=request.answer,
            context=ScoringContext(
                current_level=request.current_level.value,
                cv_skills=tuple(
                    request.cv_skills,
                ),
                recent_scores=tuple(
                    request.recent_scores,
                ),
            ),
        )

InterviewRequestMapper = RunInterviewStepPayloadMapper