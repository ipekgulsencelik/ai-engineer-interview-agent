class LLMJudgeRAGEvaluator:

    def evaluate(
        self,
        *,
        request: LLMJudgeRequest,
    ) -> float:

        prompt = (
            self._prompt_builder.build(
                request=request,
            )
        )

        response = (
            self._llm_client.generate(
                prompt=prompt,
            )
        )

        result = (
            self._response_parser.parse(
                response=response,
            )
        )

        return result.score