from dataclasses import dataclass

from kernel_rag.models.retrieval_result import RetrievalResult


@dataclass(frozen=True, slots=True)
class RAGResponse:
    answer: str
    sources: list[RetrievalResult]
