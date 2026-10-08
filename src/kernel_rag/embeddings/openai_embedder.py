from __future__ import annotations

from collections.abc import Sequence


class OpenAIEmbedder:
    def __init__(self, api_key: str, model: str, *, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError("OpenAI API key must not be empty.")
        from openai import OpenAI

        self.model = model
        self._client = OpenAI(api_key=api_key, timeout=timeout, max_retries=2)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        cleaned = [text.strip() for text in texts]
        if not cleaned or any(not text for text in cleaned):
            raise ValueError("Embedding inputs must contain non-empty text.")
        response = self._client.embeddings.create(
            model=self.model,
            input=cleaned,
            encoding_format="float",
        )
        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]

    def embed_query(self, query: str) -> list[float]:
        query = query.strip()
        if not query:
            raise ValueError("Query must not be empty.")
        return self.embed_documents([query])[0]
