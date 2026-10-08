# Architecture

## Why this design

This project is intentionally a small modular monolith. The workshop is about RAG, so the architecture keeps each RAG stage visible without introducing a separate REST API, agents, LangChain chains, or microservices.

## Offline ingestion

```text
Kernel PDF
  -> PyMuPDF block extraction
  -> structure-aware semantic chunking
  -> OpenAI embeddings
  -> Chroma PersistentClient (cosine distance)
```

## Online query

```text
Question
  -> OpenAI query embedding
  -> Chroma Top-K retrieval
  -> optional distance threshold
  -> grounded prompt construction
  -> OpenAI Responses API
  -> answer + retrieval details
```

## Important boundaries

- `app/` is UI only.
- `ingestion/` knows about PDFs and chunks, not OpenAI generation.
- `embeddings/` owns embedding API calls.
- `vector_store/` owns Chroma persistence/search.
- `retrieval/` owns retrieval policy.
- `generation/` owns prompt construction and text generation.
- `pipeline/` is the high-level Retrieve -> Augment -> Generate orchestration.

## Chunking strategy

The source PDF is curated and has strong semantic structure. We therefore preserve numbered sections and only split the three sections with independent subtopics:

- Section 3 -> Deep Learning / Natural Language Processing
- Section 10 -> AI Solutions / AI Consulting / Technical Solutions / Intelligent Automation
- Section 12 -> Kernel Team / Kernel AI Approach / SalahAldeen Current Professional Focus

This produces 18 chunks from the current PDF, with zero arbitrary text overlap. Each vector receives section/subsection titles in the text sent to the embedding model, while Chroma also stores source/page metadata for citations and workshop inspection.
