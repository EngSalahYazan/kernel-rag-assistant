from kernel_rag.generation.prompt_builder import PromptBuilder
from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.models.retrieval_result import RetrievalResult


def test_prompt_contains_grounding_and_source_context():
    builder = PromptBuilder()
    chunk = DocumentChunk(
        id="x", text="Kernel operates in Jordan and Saudi Arabia.", source="kb.pdf",
        section="8. About Kernel", subsection=None, page_start=5, page_end=5
    )
    prompt = builder.build_input("Where does Kernel operate?", [RetrievalResult(chunk, 0.1)])
    assert "Kernel operates in Jordan and Saudi Arabia." in prompt
    assert "8. About Kernel" in prompt
    assert "Where does Kernel operate?" in prompt
    assert builder.NO_ANSWER_TEXT in builder.instructions
