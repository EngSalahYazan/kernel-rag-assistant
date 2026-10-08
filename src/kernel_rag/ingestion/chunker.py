from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from kernel_rag.models.document_chunk import DocumentChunk
from kernel_rag.models.page_block import PageBlock


@dataclass(frozen=True, slots=True)
class _SectionBlock:
    text: str
    page: int


class StructureAwareChunker:
    """Create semantic chunks from the curated Kernel knowledge base.

    Major numbered sections are always preserved. Only sections that contain
    clearly independent semantic subsections are split further. There is no
    arbitrary character-based overlap.
    """

    SECTION_RE = re.compile(r"^(?P<number>\d{1,2})\.\s+(?P<title>.+)$")

    SUBHEADINGS: dict[int, tuple[str, ...]] = {
        3: ("Deep Learning", "Natural Language Processing"),
        10: (
            "Artificial Intelligence Solutions",
            "AI Consulting",
            "Technical Solutions",
            "Intelligent Automation",
        ),
        12: (
            "Kernel Team",
            "Kernel's AI Approach",
            "SalahAldeen's Current Professional Focus",
        ),
    }

    def chunk(self, blocks: list[PageBlock], source: str | Path) -> list[DocumentChunk]:
        source_name = Path(source).name
        sections = self._group_sections(blocks)
        chunks: list[DocumentChunk] = []

        for number, title, section_blocks in sections:
            subheadings = self.SUBHEADINGS.get(number)
            if subheadings:
                chunks.extend(self._split_subsections(number, title, section_blocks, subheadings, source_name))
            else:
                chunks.append(self._make_chunk(number, title, None, section_blocks, source_name, part=1))

        if not chunks:
            raise ValueError("No numbered knowledge-base sections were detected in the PDF.")
        return chunks

    def _group_sections(self, blocks: list[PageBlock]) -> list[tuple[int, str, list[_SectionBlock]]]:
        sections: list[tuple[int, str, list[_SectionBlock]]] = []
        current_number: int | None = None
        current_title: str | None = None
        current_blocks: list[_SectionBlock] = []

        for block in blocks:
            match = self.SECTION_RE.match(block.text)
            if match:
                if current_number is not None and current_title is not None:
                    sections.append((current_number, current_title, current_blocks))
                current_number = int(match.group("number"))
                current_title = match.group("title").strip()
                current_blocks = []
                continue

            # Ignore cover/purpose content before section 1.
            if current_number is not None:
                current_blocks.append(_SectionBlock(text=block.text, page=block.page))

        if current_number is not None and current_title is not None:
            sections.append((current_number, current_title, current_blocks))
        return sections

    def _split_subsections(
        self,
        number: int,
        title: str,
        blocks: list[_SectionBlock],
        subheadings: tuple[str, ...],
        source_name: str,
    ) -> list[DocumentChunk]:
        heading_set = set(subheadings)
        chunks: list[DocumentChunk] = []
        current_heading: str | None = None
        current: list[_SectionBlock] = []
        part = 0

        for block in blocks:
            if block.text in heading_set:
                if current_heading is not None and current:
                    part += 1
                    chunks.append(self._make_chunk(number, title, current_heading, current, source_name, part))
                current_heading = block.text
                current = []
            else:
                # Any lead-in text before the first subsection remains attached
                # to the first subsection rather than becoming a tiny chunk.
                current.append(block)

        if current:
            part += 1
            chunks.append(self._make_chunk(number, title, current_heading, current, source_name, part))
        return chunks

    @staticmethod
    def _slug(text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
        return slug[:55]

    def _make_chunk(
        self,
        number: int,
        section: str,
        subsection: str | None,
        blocks: list[_SectionBlock],
        source_name: str,
        part: int,
    ) -> DocumentChunk:
        if not blocks:
            raise ValueError(f"Section {number} ({section}) has no content.")
        body = "\n\n".join(block.text for block in blocks).strip()
        label = subsection or section
        chunk_id = f"s{number:02d}_{self._slug(label)}_{part:02d}"
        return DocumentChunk(
            id=chunk_id,
            text=body,
            source=source_name,
            section=f"{number}. {section}",
            subsection=subsection,
            page_start=min(block.page for block in blocks),
            page_end=max(block.page for block in blocks),
        )
