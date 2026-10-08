from __future__ import annotations

import argparse
import json
from pathlib import Path

from kernel_rag.config import get_settings
from kernel_rag.embeddings.openai_embedder import OpenAIEmbedder
from kernel_rag.ingestion.chunker import StructureAwareChunker
from kernel_rag.ingestion.pdf_loader import PDFLoader
from kernel_rag.vector_store.chroma_store import ChromaVectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest the Kernel workshop PDF into Chroma.")
    parser.add_argument("--rebuild", action="store_true", help="Delete and recreate the collection first.")
    args = parser.parse_args()

    settings = get_settings()
    api_key = settings.require_api_key()

    print(f"Loading: {settings.pdf_path}")
    blocks = PDFLoader().load(settings.pdf_path)
    chunks = StructureAwareChunker().chunk(blocks, settings.pdf_path)
    print(f"Created {len(chunks)} semantic chunks.")

    settings.processed_chunks_path.parent.mkdir(parents=True, exist_ok=True)
    settings.processed_chunks_path.write_text(
        json.dumps([chunk.to_dict() for chunk in chunks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved chunk preview: {settings.processed_chunks_path}")

    embedder = OpenAIEmbedder(api_key=api_key, model=settings.embedding_model)
    embeddings = embedder.embed_documents([chunk.embedding_text for chunk in chunks])
    print(f"Generated {len(embeddings)} embeddings using {settings.embedding_model}.")

    store = ChromaVectorStore(settings.chroma_path, settings.chroma_collection)
    if args.rebuild:
        store.rebuild()
    store.upsert(chunks, embeddings)
    print(f"Chroma collection '{settings.chroma_collection}' now contains {store.count()} records.")
    print("Ingestion complete.")


if __name__ == "__main__":
    main()
