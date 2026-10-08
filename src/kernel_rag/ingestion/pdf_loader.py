from __future__ import annotations

import re
from pathlib import Path

try:
    import pymupdf
except ImportError:  # compatibility with older PyMuPDF import name
    import fitz as pymupdf  # type: ignore

from kernel_rag.models.page_block import PageBlock


class PDFLoader:
    """Extract ordered text blocks while preserving page numbers.

    The workshop PDF has a clean single-column layout. Direct PyMuPDF block
    extraction is deterministic, transparent, and preserves the boundaries we
    need for structure-aware chunking.
    """

    IGNORED_EXACT = {
        "KERNEL | KNOWLEDGE BASE",
        "RAG Workshop Demo Dataset | August 2026",
        "PROFILE",
        "TECHNICAL BACKGROUND",
        "SELECTED PROJECT",
        "PROFESSIONAL ROLE",
        "CURRENT PROJECT",
        "AI SAFETY",
        "COMPANY",
        "TRAINING",
        "COMPANY & CAREER",
        "End of Knowledge Base",
    }

    def load(self, path: str | Path) -> list[PageBlock]:
        pdf_path = Path(path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        blocks: list[PageBlock] = []
        with pymupdf.open(pdf_path) as document:
            for page_index, page in enumerate(document):
                page_number = page_index + 1
                raw_blocks = sorted(page.get_text("blocks"), key=lambda b: (round(b[1], 1), round(b[0], 1)))
                for block in raw_blocks:
                    text = self._normalize_block(block[4])
                    if not text or text in self.IGNORED_EXACT:
                        continue
                    blocks.append(PageBlock(text=text, page=page_number))
        return blocks

    @staticmethod
    def _normalize_block(text: str) -> str:
        text = text.replace("\uf0b7", "\n- ")
        # Repair words split by a layout line break: Retrieval-\nAugmented -> Retrieval-Augmented.
        text = re.sub(r"([A-Za-z])-\s*\n\s*([A-Za-z])", r"\1-\2", text)
        lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        if not lines:
            return ""

        # Keep real bullet lists readable; reflow ordinary PDF line wrapping.
        if any(line.startswith("-") for line in lines):
            out: list[str] = []
            current = ""
            for line in lines:
                if line.startswith("-"):
                    if current:
                        out.append(current)
                    current = line
                else:
                    current = f"{current} {line}".strip()
            if current:
                out.append(current)
            return "\n".join(out)

        return " ".join(lines)
