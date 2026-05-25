# FailWise — Tech Stack

## Overview

| Layer | Tool | Version |
|---|---|---|
| Language | Python | 3.11+ |
| RAG framework | LangChain | latest |
| Vector store | ChromaDB | latest |
| Embeddings | OpenAI text-embedding-3-small | — |
| LLM | GPT-4o-mini | — |
| Backend | FastAPI | latest |
| Frontend | Streamlit | latest |
| PDF parsing | PyPDF | latest |
| Deployment — backend | Render | free tier |
| Deployment — frontend | Streamlit Cloud | free tier |

---

## Layer-by-layer decisions

### Python 3.11+
LangChain and ChromaDB both work best on 3.11+. Async support in FastAPI is
cleaner on newer versions.

### LangChain
Chosen for its beginner-friendly abstractions around embedding, retrieval, and
chain construction. The `RetrievalQA` and `Chroma` integrations reduce boilerplate
significantly for a v1. Swap for LlamaIndex in v2 if you need more control over
the ingestion pipeline.

### ChromaDB
Runs locally with zero infrastructure setup. Persists to disk at `chroma_store/`.
Supports metadata filtering natively, which is central to FailWise's hybrid
retrieval design. The main limitation is that it does not scale horizontally —
acceptable for a portfolio project, swap for Pinecone when you need cloud
persistence.

### OpenAI text-embedding-3-small
Cheap (roughly $0.02 per 1M tokens), fast, and good enough for this corpus size.
Dimensionality of 1536. If you want to go fully open source, swap for
`sentence-transformers/all-MiniLM-L6-v2` via HuggingFace — free, runs locally,
slightly lower quality.

### GPT-4o-mini
Fast and cheap for prototyping — about 15x cheaper than GPT-4o with acceptable
quality for Q&A over structured text. The system prompt keeps it grounded to
retrieved context only.

### FastAPI
Async, lightweight, and auto-generates OpenAPI docs at `/docs` out of the box.
Industry standard for Python APIs. The `/query` endpoint is the only route needed
for v1.

### Streamlit
Fastest way to ship a usable UI without writing any frontend code. Sufficient for
a portfolio demo. Swap for a React frontend in v2 if you want to show full-stack
breadth.

### PyPDF
Handles PDF text extraction for the ingestion pipeline. Falls back gracefully on
malformed PDFs. Combined with standard markdown parsing for `.md` files.

---

## Open source alternatives (if you want zero API costs)

| Component | Paid (default) | Free alternative |
|---|---|---|
| Embeddings | OpenAI text-embedding-3-small | all-MiniLM-L6-v2 (HuggingFace) |
| LLM | GPT-4o-mini | Ollama + Mistral 7B (local) |
| Vector store | ChromaDB (local) | FAISS (no metadata filtering) |

Note: running Ollama locally requires a decent machine (8GB+ RAM). For a
portfolio project the OpenAI costs are minimal — embedding 20 postmortems costs
under $0.01.

---

## Environment variables

```env
OPENAI_API_KEY=your_key_here
CHROMA_PERSIST_DIR=./chroma_store
```

---

## Dependencies

```txt
langchain
langchain-openai
chromadb
openai
fastapi
uvicorn
streamlit
pypdf
python-dotenv
```

Install with:

```bash
pip install -r requirements.txt
```