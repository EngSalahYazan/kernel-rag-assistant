from __future__ import annotations

from typing import Protocol

from kernel_rag.models.retrieval_result import RetrievalResult


class _QueryEmbedder(Protocol):
    def embed_query(self, query: str) -> list[float]: ...


class _SearchStore(Protocol):
    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievalResult]: ...


class Retriever:
    def __init__(
        self,
        embedder: _QueryEmbedder,
        vector_store: _SearchStore,
        *,
        top_k: int = 3,
        distance_threshold: float | None = None,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k
        self.distance_threshold = distance_threshold

    def retrieve(self, query: str) -> list[RetrievalResult]:
        query = query.strip()
        if not query:
            return []
        query_embedding = self.embedder.embed_query(query)
        results = self.vector_store.search(query_embedding, self.top_k)
        if self.distance_threshold is None:
            return results
        return [result for result in results if result.distance <= self.distance_threshold]
