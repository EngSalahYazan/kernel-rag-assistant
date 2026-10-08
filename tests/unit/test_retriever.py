from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.models.retrieval_result import RetrievalResult
from kernel_rag.retrieval.retriever import Retriever


class FakeEmbedder:
    def embed_query(self, query: str) -> list[float]:
        return [1.0, 0.0]


class FakeStore:
    def search(self, query_embedding, top_k):
        chunk = DocumentChunk("1", "text", "kb.pdf", "1. Section", None, 1, 1)
        return [RetrievalResult(chunk, 0.2), RetrievalResult(chunk, 0.8)]


def test_threshold_filters_results():
    retriever = Retriever(FakeEmbedder(), FakeStore(), top_k=3, distance_threshold=0.5)
    results = retriever.retrieve("hello")
    assert len(results) == 1
    assert results[0].distance == 0.2

def test_empty_query_returns_no_results():
    assert Retriever(FakeEmbedder(), FakeStore()).retrieve("   ") == []
