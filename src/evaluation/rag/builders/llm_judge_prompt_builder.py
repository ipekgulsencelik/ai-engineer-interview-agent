class LLMJudgePromptBuilder:

    @staticmethod
    def build(
        *,
        request: LLMJudgeRequest,
    ) -> str:
        ...