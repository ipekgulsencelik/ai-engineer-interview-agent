class LLMJudgeResponseParser:

    @staticmethod
    def parse(
        *,
        response: str,
    ) -> LLMJudgeResult:
        ...