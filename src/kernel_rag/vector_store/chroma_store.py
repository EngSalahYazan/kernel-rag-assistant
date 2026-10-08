from __future__ import annotations

from pathlib import Path
from typing import Any

from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.models.retrieval_result import RetrievalResult


class ChromaVectorStore:
    def __init__(self, path: str | Path, collection_name: str) -> None:
        import chromadb

        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self._client = chromadb.PersistentClient(path=str(self.path))
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=None,
            configuration={"hnsw": {"space": "cosine"}},
        )

    def count(self) -> int:
        return self._collection.count()

    def rebuild(self) -> None:
        try:
            self._client.delete_collection(name=self.collection_name)
        except Exception:
            # Safe for a first run where the collection does not yet exist.
            pass
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=None,
            configuration={"hnsw": {"space": "cosine"}},
        )

    def upsert(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match.")
        if not chunks:
            raise ValueError("Cannot upsert an empty chunk list.")

        self._collection.upsert(
            ids=[chunk.id for chunk in chunks],
            embeddings=embeddings,
            documents=[chunk.text for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
        )

    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievalResult]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        result: dict[str, Any] = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        ids = (result.get("ids") or [[]])[0]
        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]

        output: list[RetrievalResult] = []
        for chunk_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            metadata = metadata or {}
            chunk = DocumentChunk(
                id=str(chunk_id),
                text=str(document or ""),
                source=str(metadata.get("source", "")),
                section=str(metadata.get("section", "")),
                subsection=str(metadata.get("subsection", "")) or None,
                page_start=int(metadata.get("page_start", 0)),
                page_end=int(metadata.get("page_end", 0)),
            )
            output.append(RetrievalResult(chunk=chunk, distance=float(distance)))
        return output
