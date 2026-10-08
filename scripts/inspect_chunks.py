from __future__ import annotations

import json

from kernel_rag.config import get_settings
from kernel_rag.ingestion.chunker import StructureAwareChunker
from kernel_rag.ingestion.pdf_loader import PDFLoader


def main() -> None:
    settings = get_settings()
    blocks = PDFLoader().load(settings.pdf_path)
    chunks = StructureAwareChunker().chunk(blocks, settings.pdf_path)

    for chunk in chunks:
        page = str(chunk.page_start) if chunk.page_start == chunk.page_end else f"{chunk.page_start}-{chunk.page_end}"
        print("=" * 88)
        print(f"ID: {chunk.id}")
        print(f"Section: {chunk.section}")
        print(f"Subsection: {chunk.subsection or '-'}")
        print(f"Page: {page}")
        print(f"Characters: {len(chunk.text)}")
        print("-" * 88)
        print(chunk.text)
        print()

    settings.processed_chunks_path.parent.mkdir(parents=True, exist_ok=True)
    settings.processed_chunks_path.write_text(
        json.dumps([chunk.to_dict() for chunk in chunks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nTotal chunks: {len(chunks)}")
    print(f"Saved: {settings.processed_chunks_path}")


if __name__ == "__main__":
    main()
