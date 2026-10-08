from dataclasses import dataclass

from kernel_rag.models.document_chunk import DocumentChunk


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    chunk: DocumentChunk
    distance: float

    @property
    def similarity(self) -> float:
        # Chroma cosine distance = 1 - cosine_similarity.
        return max(-1.0, min(1.0, 1.0 - self.distance))
