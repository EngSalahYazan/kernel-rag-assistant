# Test Report

Generated for the Kernel Knowledge Assistant workshop build.

## Automated offline verification

Status: **PASS**

The following checks were executed against the generated project:

- Python source compilation (`src`, `app`, `scripts`, and `tests`)
- Real PDF extraction using the included `Kernel_Knowledge_Base_RAG_Workshop.pdf`
- Repeated header/footer removal
- Structure-aware section detection
- Exact semantic chunk count: **18**
- Cross-page section handling (for example, Current Role and MABIEN Governance)
- Semantic subsection splitting for sections 3, 10, and 12
- Prompt grounding construction
- Retrieval distance-threshold filtering
- RAG pipeline orchestration using test doubles
- OpenAI Embeddings API adapter call shape using a fake SDK client
- OpenAI Responses API adapter call shape using a fake SDK client
- Chroma PersistentClient / cosine collection / upsert / query adapter call shape using a fake Chroma module

Pytest result during build:

```text
9 passed
```

## Real source-PDF result

```text
Extracted blocks: 84
Semantic chunks: 18
```

The generated chunk preview is included at:

```text
data/processed/chunks.json
```

## What was intentionally not executed

A live OpenAI API request was not executed because the delivered `.env` intentionally contains an empty `OPENAI_API_KEY`.

A live dependency installation / Chroma runtime was also not possible in the build sandbox because package-download network access was unavailable. The OpenAI and Chroma adapters were therefore verified with automated contract-style test doubles and checked against the current official API documentation.

## Final user-side acceptance test

After adding the OpenAI key, run:

```powershell
python scripts/ingest.py --rebuild
python scripts/evaluate.py
streamlit run app/streamlit_app.py
```

Then test at least one direct question, one semantic question, one multi-context question, and one deliberately unanswerable question.
