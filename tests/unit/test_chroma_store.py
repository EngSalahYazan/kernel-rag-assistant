import sys
from types import SimpleNamespace

from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.vector_store.chroma_store import ChromaVectorStore


class _FakeCollection:
    def __init__(self):
        self.records = []
        self.last_query = None

    def count(self):
        return len(self.records)

    def upsert(self, **kwargs):
        self.records = list(kwargs["ids"])
        self.last_upsert = kwargs

    def query(self, **kwargs):
        self.last_query = kwargs
        return {
            "ids": [["s01"]],
            "documents": [["Kernel is a technology company."]],
            "metadatas": [[{
                "source": "kb.pdf",
                "section": "8. About Kernel",
                "subsection": "",
                "page_start": 5,
                "page_end": 5,
            }]],
            "distances": [[0.12]],
        }


class _FakeClient:
    def __init__(self, path):
        self.path = path
        self.collection = _FakeCollection()
        self.create_calls = []
        self.deleted = []

    def get_or_create_collection(self, **kwargs):
        self.create_calls.append(kwargs)
        return self.collection

    def delete_collection(self, name):
        self.deleted.append(name)
        self.collection = _FakeCollection()


class _FakeChromaModule:
    clients = []

    @classmethod
    def PersistentClient(cls, path):
        client = _FakeClient(path)
        cls.clients.append(client)
        return client


def test_chroma_store_uses_persistent_cosine_collection(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "chromadb", _FakeChromaModule)
    store = ChromaVectorStore(tmp_path / "db", "kernel_knowledge")
    client = _FakeChromaModule.clients[-1]
    assert client.create_calls[0]["embedding_function"] is None
    assert client.create_calls[0]["configuration"] == {"hnsw": {"space": "cosine"}}

    chunk = DocumentChunk("s01", "Kernel is a technology company.", "kb.pdf", "8. About Kernel", None, 5, 5)
    store.upsert([chunk], [[1.0, 0.0]])
    assert store.count() == 1

    results = store.search([1.0, 0.0], top_k=3)
    assert len(results) == 1
    assert results[0].chunk.section == "8. About Kernel"
    assert results[0].distance == 0.12
    assert client.collection.last_query["query_embeddings"] == [[1.0, 0.0]]
    assert client.collection.last_query["n_results"] == 3
