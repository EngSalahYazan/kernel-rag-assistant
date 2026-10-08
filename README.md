# Kernel Knowledge Assistant

A transparent Retrieval-Augmented Generation (RAG) demo built for the **RAG in Action** workshop.

The assistant answers questions about **SalahAldeen Yazan Salah AlNaimat, Kernel, MABIEN, Kernel services, projects, clients, team, and AI training programs** using only the included Kernel knowledge-base PDF.

## What the project demonstrates

```text
Kernel PDF
   ↓
PyMuPDF block extraction
   ↓
Structure-aware semantic chunking
   ↓
OpenAI Embeddings
   ↓
Chroma Persistent Vector Store
   ↓
User Question
   ↓
Query Embedding
   ↓
Top-K Semantic Retrieval
   ↓
Grounded Prompt
   ↓
OpenAI Responses API
   ↓
Answer + Sources + Retrieval Details
```

The implementation intentionally avoids LangChain chains, agents, FastAPI, and microservices so the workshop audience can see the RAG mechanics directly.

---

## Tech stack

- Python 3.11–3.12
- OpenAI Responses API
- `gpt-5.6-terra` by default
- `text-embedding-3-small`
- Chroma `PersistentClient`
- PyMuPDF
- Streamlit
- Pytest

---

## Project structure

```text
kernel-rag-assistant/
│
├── app/
│   └── streamlit_app.py
│
├── src/kernel_rag/
│   ├── config.py
│   ├── bootstrap.py
│   ├── exceptions.py
│   ├── models/
│   ├── ingestion/
│   ├── embeddings/
│   ├── vector_store/
│   ├── retrieval/
│   ├── generation/
│   ├── pipeline/
│   └── evaluation/
│
├── scripts/
│   ├── ingest.py
│   ├── inspect_chunks.py
│   └── evaluate.py
│
├── data/
│   ├── raw/
│   │   └── Kernel_Knowledge_Base_RAG_Workshop.pdf
│   └── processed/
│       └── chunks.json
│
├── storage/chroma/
├── evaluation/questions.json
├── tests/
├── docs/ARCHITECTURE.md
├── .env
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Quick start on Windows PowerShell

## 1. Open the project

```powershell
cd kernel-rag-assistant
```

## 2. Create a Python 3.11 virtual environment

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies and the local package

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps
```

## 4. Add your OpenAI API key

Open `.env` and replace the blank value:

```env
OPENAI_API_KEY=
```

with your own key:

```env
OPENAI_API_KEY=YOUR_KEY_HERE
```

Do not commit `.env` to Git. It is already ignored.

The default configuration is:

```env
OPENAI_LLM_MODEL=gpt-5.6-terra
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_REASONING_EFFORT=low
OPENAI_MAX_OUTPUT_TOKENS=500
RAG_TOP_K=3
RAG_DISTANCE_THRESHOLD=
```

Leave `RAG_DISTANCE_THRESHOLD` blank for the first version. Tune it only after observing retrieval distances during evaluation.

---

# Inspect the chunks before calling OpenAI

This step makes **no OpenAI API calls**.

```powershell
python scripts/inspect_chunks.py
```

The current PDF should produce **18 semantic chunks**.

A JSON copy is written to:

```text
data/processed/chunks.json
```

This is useful during the workshop because you can show exactly what the PDF became before embeddings were generated.

---

# Ingest the knowledge base

Run:

```powershell
python scripts/ingest.py --rebuild
```

This performs:

```text
PDF
→ structured blocks
→ 18 semantic chunks
→ OpenAI embeddings
→ Chroma local persistence
```

The Chroma database is stored in:

```text
storage/chroma/
```

You normally run ingestion once before the workshop unless the source PDF changes.

---

# Run the app

```powershell
streamlit run app/streamlit_app.py
```

The browser should open the **Kernel Knowledge Assistant**.

The UI displays:

- grounded answer
- retrieved section
- subsection when available
- page number
- cosine similarity
- cosine distance
- exact retrieved text

This makes the retrieval process visible during the workshop.

---

# Recommended demo questions

## Direct retrieval

```text
Where did SalahAldeen study and what did he study?
```

## Semantic retrieval

```text
Has SalahAldeen worked with transformer-based language models?
```

## Project question

```text
How does the AI lead qualification system prioritize important customers?
```

## Healthcare RAG / multi-agent question

```text
What does MABIEN do and who makes the final insurance decision?
```

## Governance question

```text
How does MABIEN reduce hallucination risk?
```

## Company question

```text
Where does Kernel operate and what is its relationship with Falak Investment?
```

## Services question phrased differently from the document

```text
Can Kernel help a company automate repetitive operational work?
```

## Training question

```text
What AI training programs does Kernel provide?
```

## No-answer / hallucination demo

```text
What is SalahAldeen's favorite football club?
```

Expected behavior: the assistant should state that the information is not available in the Kernel Knowledge Base rather than inventing an answer.

---

# Evaluation

After ingestion, run:

```powershell
python scripts/evaluate.py
```

The initial evaluation focuses on **retrieval hit rate**: whether the expected section appears in the Top-K results.

The dataset is located at:

```text
evaluation/questions.json
```

The dataset also contains deliberately unanswerable questions for later no-answer threshold experiments.

---

# Run tests

```powershell
pytest
```

The included tests validate:

- real PDF extraction
- removal of repeated headers/footers
- exact expected 18 semantic chunks
- expected semantic subsections
- retrieval threshold behavior
- grounded prompt construction
- high-level Retrieve → Augment → Generate orchestration

The automated tests do **not** require a real OpenAI API key.

---

# Why PyMuPDF directly instead of PyMuPDF4LLM?

The final workshop PDF is a clean, single-column, curated document with reliable text blocks and explicit section headings. After testing the actual PDF, direct PyMuPDF block extraction was simpler and more deterministic for this dataset than adding another parsing abstraction.

This also makes the ingestion stage easier to explain in a one-hour RAG workshop.

If the project later needs to ingest complex multi-column PDFs, scanned documents, tables, or heterogeneous documents, the loader can be replaced without changing the retrieval or generation layers.

---

# Chunking strategy

The project uses **structure-aware semantic chunking**, not arbitrary fixed-size character splitting.

The numbered sections are preserved. Only semantically independent sections are split further:

```text
3. Deep Learning and NLP Experience
   ├── Deep Learning
   └── Natural Language Processing

10. Kernel Services and Solutions
   ├── Artificial Intelligence Solutions
   ├── AI Consulting
   ├── Technical Solutions
   └── Intelligent Automation

12. Team, Approach, and Current Focus
   ├── Kernel Team
   ├── Kernel's AI Approach
   └── SalahAldeen's Current Professional Focus
```

The current document produces exactly **18 chunks**.

No arbitrary text overlap is used in V1 because each chunk already represents a complete semantic unit.

---

# Retrieval strategy

The first version intentionally keeps retrieval simple:

```text
Query
→ OpenAI query embedding
→ Chroma cosine vector search
→ Top 3 chunks
```

No reranker and no hybrid BM25 search are used initially because the knowledge base is small.

`RAG_DISTANCE_THRESHOLD` is disabled by default. Do not choose a threshold from a tutorial. First collect retrieval distances for relevant and irrelevant questions, then choose a threshold from evidence.

---

# Grounding behavior

The LLM receives only the retrieved chunks plus the user question and is explicitly instructed not to invent facts about:

- SalahAldeen
- Kernel
- MABIEN
- Kernel clients
- services
- projects
- locations
- team
- training programs

If the retrieved context is insufficient, the requested fallback is:

```text
I couldn't find this information in the Kernel Knowledge Base.
```

This is a prompt-level safeguard, not a mathematical guarantee. Evaluation is still required.

---

# Architecture extension points

The project is deliberately modular so future upgrades do not require rewriting the whole application.

Possible later upgrades:

```text
Chroma → Qdrant / Pinecone / pgvector
Top-K retrieval → threshold + reranking
Dense search → hybrid dense + BM25
Single PDF → multi-document ingestion
Streamlit → frontend + FastAPI
Basic RAG → agentic RAG / LangGraph
```

For the current one-hour workshop, these are intentionally out of scope.

---

# Troubleshooting

## `OPENAI_API_KEY is empty`

Add the key to `.env` and restart the command/app.

## `The Chroma collection is empty`

Run:

```powershell
python scripts/ingest.py --rebuild
```

## `ModuleNotFoundError: kernel_rag`

Run from the project root and install the local package:

```powershell
pip install -e . --no-deps
```

## You changed the PDF

Re-run:

```powershell
python scripts/inspect_chunks.py
python scripts/ingest.py --rebuild
```

Then run tests and evaluation again.

---

# Suggested workshop flow

A clean one-hour presentation can use the project in this sequence:

1. Show the source PDF.
2. Show `data/processed/chunks.json`.
3. Explain embeddings.
4. Show Chroma / vector retrieval.
5. Ask a semantic question in Streamlit.
6. Expand the retrieval details and show the Top-K chunks.
7. Explain prompt augmentation.
8. Ask an unanswerable question to demonstrate grounding.
9. Run or show the evaluation results.
10. Close with future improvements: reranking, hybrid search, agentic RAG.
