from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    id: str
    text: str
    source: str
    section: str
    subsection: str | None
    page_start: int
    page_end: int

    @property
    def embedding_text(self) -> str:
        parts = [f"Section: {self.section}"]
        if self.subsection:
            parts.append(f"Subsection: {self.subsection}")
        parts.append(self.text)
        return "\n\n".join(parts)

    @property
    def metadata(self) -> dict[str, str | int]:
        return {
            "source": self.source,
            "section": self.section,
            "subsection": self.subsection or "",
            "page_start": self.page_start,
            "page_end": self.page_end,
        }

    def to_dict(self) -> dict:
        return asdict(self)
