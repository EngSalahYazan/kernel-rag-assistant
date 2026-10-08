from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from kernel_rag.exceptions import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _optional_float(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    return float(value)


@dataclass(frozen=True, slots=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    pdf_path: Path = PROJECT_ROOT / "data" / "raw" / "Kernel_Knowledge_Base_RAG_Workshop.pdf"
    processed_chunks_path: Path = PROJECT_ROOT / "data" / "processed" / "chunks.json"
    chroma_path: Path = PROJECT_ROOT / "storage" / "chroma"
    chroma_collection: str = "kernel_knowledge"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    llm_model: str = os.getenv("OPENAI_LLM_MODEL", "gpt-5.6-terra").strip()
    embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small").strip()
    reasoning_effort: str = os.getenv("OPENAI_REASONING_EFFORT", "low").strip()
    max_output_tokens: int = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "500"))
    top_k: int = int(os.getenv("RAG_TOP_K", "3"))
    distance_threshold: float | None = _optional_float(os.getenv("RAG_DISTANCE_THRESHOLD"))

    def require_api_key(self) -> str:
        if not self.openai_api_key:
            raise ConfigurationError(
                "OPENAI_API_KEY is empty. Add your key to the project .env file before ingestion or asking questions."
            )
        return self.openai_api_key


def get_settings() -> Settings:
    return Settings()
