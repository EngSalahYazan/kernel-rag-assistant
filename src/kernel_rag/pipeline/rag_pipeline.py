from __future__ import annotations

from typing import Protocol

from kernel_rag.generation.prompt_builder import PromptBuilder
from kernel_rag.models.rag_response import RAGResponse
from kernel_rag.models.retrieval_result import RetrievalResult


class _Retriever(Protocol):
    def retrieve(self, query: str) -> list[RetrievalResult]: ...


class _Generator(Protocol):
    def generate(self, *, instructions: str, input_text: str) -> str: ...


class RAGPipeline:
    def __init__(self, retriever: _Retriever, prompt_builder: PromptBuilder, generator: _Generator) -> None:
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator

    def ask(self, question: str) -> RAGResponse:
        question = question.strip()
        if not question:
            raise ValueError("Question must not be empty.")

        results = self.retriever.retrieve(question)
        if not results:
            return RAGResponse(answer=self.prompt_builder.NO_ANSWER_TEXT, sources=[])

        input_text = self.prompt_builder.build_input(question, results)
        answer = self.generator.generate(
            instructions=self.prompt_builder.instructions,
            input_text=input_text,
        )
        return RAGResponse(answer=answer, sources=results)
