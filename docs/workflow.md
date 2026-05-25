# FailWise — Workflow

## Overview

FailWise ingests engineering postmortems, chunks them by incident section, tags structured metadata, embeds them into a vector store, and exposes a retrieval chain via API. This document describes how data flows through the system end to end.

---

## Pipeline

### Step 1 — Data collection
- Download postmortems manually as PDF or markdown
- Sources: Cloudflare blog, danluu/post-mortems, AWS post-event summaries, Stripe engineering blog
- Target: 15–20 documents for v1
- Store raw files in `data/postmortems/`

### Step 2 — Document loading
- `ingest/loader.py` reads all files from `data/postmortems/`
- Supports `.pdf` and `.md` formats
- Outputs raw text per document with a source filename attached

### Step 3 — Section-aware chunking
- `ingest/chunker.py` splits each document by incident section headings
- Four chunk types: `timeline`, `root_cause`, `resolution`, `learnings`
- Falls back to paragraph splitting if headings are not detected
- Each chunk stays semantically complete — no mid-sentence or mid-thought splits

### Step 4 — Metadata tagging
- `ingest/chunker.py` also attaches structured metadata to each chunk
- Fields: `company`, `year`, `severity`, `category`, `chunk_type`
- v1: tag manually or with a lightweight extraction prompt
- v2: auto-extract with an LLM call during ingestion

### Step 5 — Embedding
- `ingest/embedder.py` sends each chunk to OpenAI `text-embedding-3-small`
- Embeddings + metadata stored in ChromaDB at `chroma_store/`
- Run once to build the index; re-run when new docs are added

### Step 6 — Retrieval
- `retrieval/retriever.py` accepts a user query
- Applies metadata filters first (company, year, category) if present in the query
- Runs semantic similarity search over the filtered subset
- Returns top-k chunks with source attribution

### Step 7 — Generation
- `retrieval/chain.py` builds a LangChain RAG chain
- Retrieved chunks are passed as context to GPT-4o-mini
- System prompt instructs the model to answer only from context, never hallucinate
- Response includes source postmortem references

### Step 8 — API layer
- `api/main.py` exposes a `/query` POST endpoint via FastAPI
- Request body: `{ "question": "...", "filters": { "company": "...", "category": "..." } }`
- Response: `{ "answer": "...", "sources": [...] }`

### Step 9 — Frontend
- `ui/app.py` is a Streamlit app
- Text input for the question
- Optional filter dropdowns for company and category
- Displays answer + expandable source chunks below

### Step 10 — Deployment
- Backend: deploy FastAPI on Render (free tier)
- Frontend: deploy Streamlit on Streamlit Cloud (free tier)
- ChromaDB: persisted locally in v1; swap for Pinecone in v2 for cloud persistence

---

## Data flow diagram

raw docs (PDF/MD)
↓
loader.py
↓
chunker.py  →  [chunk_type, company, year, severity, category]
↓
embedder.py  →  ChromaDB
↓
retriever.py  ←  user query + filters
↓
chain.py  →  GPT-4o-mini
↓
FastAPI /query
↓
Streamlit UI

---

## Design decisions

### Why section-aware chunking over fixed token windows?
Fixed windows break semantic units — a chunk could be half root cause, half resolution, which confuses the retriever. Splitting by incident section ensures each chunk has a single clear purpose and retrieves cleanly.

### Why metadata filtering?
Some constraints are structural, not semantic. "Show me Cloudflare incidents from 2023" should not rely on cosine similarity — it should be a hard filter. Metadata makes retrieval precise and explainable.

### Why ChromaDB for v1?
Zero infrastructure overhead. Runs locally, persists to disk, integrates with LangChain in three lines. Swap for Pinecone when you need cloud persistence or scale.