from __future__ import annotations

from kernel_rag.models.retrieval_result import RetrievalResult


class PromptBuilder:
    NO_ANSWER_TEXT = "I couldn't find this information in the Kernel Knowledge Base."

    @property
    def instructions(self) -> str:
        return (
            "You are the Kernel Knowledge Assistant. "
            "Answer only from the supplied Kernel Knowledge Base context. "
            "Do not use outside knowledge to invent or complete facts about SalahAldeen, Kernel, MABIEN, "
            "Kernel's clients, services, team, projects, locations, or training programs. "
            "If the context is insufficient, answer exactly: "
            f'"{self.NO_ANSWER_TEXT}" '
            "Keep answers concise and factual. When useful, synthesize information from multiple context blocks."
        )

    def build_input(self, question: str, results: list[RetrievalResult]) -> str:
        context_parts: list[str] = []
        for index, result in enumerate(results, start=1):
            chunk = result.chunk
            page_label = str(chunk.page_start) if chunk.page_start == chunk.page_end else f"{chunk.page_start}-{chunk.page_end}"
            context_parts.append(
                f"[Context {index}]\n"
                f"Section: {chunk.section}\n"
                f"Subsection: {chunk.subsection or 'N/A'}\n"
                f"Page: {page_label}\n"
                f"Text: {chunk.text}"
            )

        context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant context was retrieved."
        return f"CONTEXT\n{context}\n\nQUESTION\n{question.strip()}"
