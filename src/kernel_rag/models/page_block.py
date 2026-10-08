from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PageBlock:
    text: str
    page: int
