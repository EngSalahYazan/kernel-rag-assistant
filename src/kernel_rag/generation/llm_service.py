from __future__ import annotations


class OpenAILLMService:
    def __init__(
        self,
        api_key: str,
        model: str,
        *,
        reasoning_effort: str = "low",
        max_output_tokens: int = 500,
        timeout: float = 60.0,
    ) -> None:
        if not api_key:
            raise ValueError("OpenAI API key must not be empty.")
        from openai import OpenAI

        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens
        self._client = OpenAI(api_key=api_key, timeout=timeout, max_retries=2)

    def generate(self, *, instructions: str, input_text: str) -> str:
        response = self._client.responses.create(
            model=self.model,
            instructions=instructions,
            input=input_text,
            reasoning={"effort": self.reasoning_effort},
            max_output_tokens=self.max_output_tokens,
            store=False,
        )
        answer = (response.output_text or "").strip()
        if not answer:
            raise RuntimeError("OpenAI returned an empty response.")
        return answer
