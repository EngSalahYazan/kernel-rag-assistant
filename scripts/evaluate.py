from __future__ import annotations

import json

from kernel_rag.config import get_settings
from kernel_rag.embeddings.openai_embedder import OpenAIEmbedder
from kernel_rag.evaluation.evaluator import evaluate_retrieval
from kernel_rag.retrieval.retriever import Retriever
from kernel_rag.vector_store.chroma_store import ChromaVectorStore


def main() -> None:
    settings = get_settings()
    api_key = settings.require_api_key()
    dataset_path = settings.project_root / "evaluation" / "questions.json"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))

    embedder = OpenAIEmbedder(api_key=api_key, model=settings.embedding_model)
    store = ChromaVectorStore(settings.chroma_path, settings.chroma_collection)
    if store.count() == 0:
        raise RuntimeError("Knowledge base is empty. Run ingestion first.")
    retriever = Retriever(embedder, store, top_k=settings.top_k)

    evaluable = [item for item in dataset if item["answerable"] and item.get("expected_sections")]
    hits = 0
    for item in evaluable:
        results = retriever.retrieve(item["question"])
        report = evaluate_retrieval(item["question"], item["expected_sections"], results)
        hits += int(report.hit)
        status = "PASS" if report.hit else "FAIL"
        print(f"[{status}] {report.question}")
        print(f"  expected: {', '.join(report.expected_sections)}")
        print(f"  retrieved: {', '.join(report.retrieved_sections)}")

    rate = hits / len(evaluable) if evaluable else 0.0
    print(f"\nRetrieval hit rate: {hits}/{len(evaluable)} = {rate:.1%}")
    print("Note: tune RAG_DISTANCE_THRESHOLD only after reviewing relevant vs. irrelevant distances.")


if __name__ == "__main__":
    main()
