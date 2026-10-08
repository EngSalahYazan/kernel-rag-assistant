from __future__ import annotations

from dataclasses import dataclass

from kernel_rag.models.retrieval_result import RetrievalResult


@dataclass(frozen=True, slots=True)
class RetrievalEvaluation:
    question: str
    expected_sections: list[str]
    retrieved_sections: list[str]
    hit: bool


def evaluate_retrieval(
    question: str, expected_sections: list[str], results: list[RetrievalResult]
) -> RetrievalEvaluation:
    retrieved = [result.chunk.section for result in results]
    expected_lower = [item.lower() for item in expected_sections]
    hit = any(
        any(expected in retrieved_section.lower() for expected in expected_lower)
        for retrieved_section in retrieved
    )
    return RetrievalEvaluation(
        question=question,
        expected_sections=expected_sections,
        retrieved_sections=retrieved,
        hit=hit,
    )
