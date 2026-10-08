from __future__ import annotations

from kernel_rag.config import Settings, get_settings
from kernel_rag.embeddings.openai_embedder import OpenAIEmbedder
from kernel_rag.exceptions import KnowledgeBaseNotReadyError
from kernel_rag.generation.llm_service import OpenAILLMService
from kernel_rag.generation.prompt_builder import PromptBuilder
from kernel_rag.pipeline.rag_pipeline import RAGPipeline
from kernel_rag.retrieval.retriever import Retriever
from kernel_rag.vector_store.chroma_store import ChromaVectorStore


def build_pipeline(settings: Settings | None = None) -> RAGPipeline:
    settings = settings or get_settings()
    api_key = settings.require_api_key()

    embedder = OpenAIEmbedder(api_key=api_key, model=settings.embedding_model)
    vector_store = ChromaVectorStore(settings.chroma_path, settings.chroma_collection)
    if vector_store.count() == 0:
        raise KnowledgeBaseNotReadyError(
            "The Chroma collection is empty. Run `python scripts/ingest.py --rebuild` first."
        )

    retriever = Retriever(
        embedder,
        vector_store,
        top_k=settings.top_k,
        distance_threshold=settings.distance_threshold,
    )
    generator = OpenAILLMService(
        api_key=api_key,
        model=settings.llm_model,
        reasoning_effort=settings.reasoning_effort,
        max_output_tokens=settings.max_output_tokens,
    )
    return RAGPipeline(retriever, PromptBuilder(), generator)
