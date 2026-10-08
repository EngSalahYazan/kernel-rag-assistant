from pathlib import Path

from kernel_rag.ingestion.chunker import StructureAwareChunker
from kernel_rag.ingestion.pdf_loader import PDFLoader


def test_real_workshop_pdf_creates_expected_semantic_chunks():
    root = Path(__file__).resolve().parents[2]
    pdf = root / "data" / "raw" / "Kernel_Knowledge_Base_RAG_Workshop.pdf"
    chunks = StructureAwareChunker().chunk(PDFLoader().load(pdf), pdf)

    assert len(chunks) == 18
    assert chunks[0].section == "1. About SalahAldeen"
    assert any(chunk.subsection == "Natural Language Processing" for chunk in chunks)
    assert any(chunk.subsection == "Intelligent Automation" for chunk in chunks)
    assert any(chunk.subsection == "Kernel's AI Approach" for chunk in chunks)
    assert all(chunk.text.strip() for chunk in chunks)
    assert all(chunk.page_start <= chunk.page_end for chunk in chunks)


def test_loader_removes_repeated_header_and_footer():
    root = Path(__file__).resolve().parents[2]
    pdf = root / "data" / "raw" / "Kernel_Knowledge_Base_RAG_Workshop.pdf"
    text = "\n".join(block.text for block in PDFLoader().load(pdf))
    assert "KERNEL | KNOWLEDGE BASE" not in text
    assert "RAG Workshop Demo Dataset | August 2026" not in text
