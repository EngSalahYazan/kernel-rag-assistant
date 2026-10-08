from kernel_rag.generation.prompt_builder import PromptBuilder
from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.models.retrieval_result import RetrievalResult
from kernel_rag.pipeline.rag_pipeline import RAGPipeline


class FakeRetriever:
    def retrieve(self, query):
        chunk = DocumentChunk(
            "s01", "He studied Computer Engineering at The Hashemite University.",
            "kb.pdf", "1. About SalahAldeen", None, 2, 2
        )
        return [RetrievalResult(chunk, 0.1)]


class FakeGenerator:
    def generate(self, *, instructions, input_text):
        assert "Kernel Knowledge Assistant" in instructions
        assert "Hashemite University" in input_text
        return "He studied Computer Engineering at The Hashemite University."


def test_pipeline_orchestrates_retrieve_augment_generate():
    pipeline = RAGPipeline(FakeRetriever(), PromptBuilder(), FakeGenerator())
    response = pipeline.ask("Where did SalahAldeen study?")
    assert "Hashemite University" in response.answer
    assert len(response.sources) == 1
