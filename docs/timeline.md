# FailWise — Build Timeline

Target: ship a working demo in 6 days.

---

## Day 1 — Data collection

- [ ] Read through danluu/post-mortems on GitHub
- [ ] Download 15–20 postmortems as PDF or markdown
- [ ] Organize into `data/postmortems/` folder
- [ ] Skim each one and note which section headings they use
- [ ] Create a simple spreadsheet or markdown table tracking: filename, company, year, severity, category

**Done when:** `data/postmortems/` has at least 15 documents and you have metadata noted for each.

---

## Day 2 — Ingestion pipeline

- [ ] Set up project folder structure
- [ ] Install dependencies: `langchain`, `chromadb`, `openai`, `pypdf`, `fastapi`, `streamlit`
- [ ] Write `ingest/loader.py` — loads PDFs and markdowns, returns raw text
- [ ] Write `ingest/chunker.py` — splits by section headings, attaches metadata
- [ ] Test chunker on 3–4 docs manually, inspect output

**Done when:** chunker correctly splits a postmortem into labelled sections with metadata attached.

---

## Day 3 — Embedding and vector store

- [ ] Write `ingest/embedder.py`
- [ ] Connect to OpenAI embeddings API
- [ ] Load all chunks + metadata into ChromaDB
- [ ] Run the pipeline on all 15–20 docs
- [ ] Open ChromaDB and verify chunks and metadata look correct

**Done when:** ChromaDB is populated and you can do a raw similarity query from a Python script and get sensible results.

---

## Day 4 — Retrieval chain

- [ ] Write `retrieval/retriever.py` — metadata filter + semantic search
- [ ] Write `retrieval/chain.py` — LangChain RAG chain with GPT-4o-mini
- [ ] Test 5–6 questions from the terminal
- [ ] Tune the system prompt so answers cite sources and don't hallucinate

**Done when:** asking "What monitoring gaps appear most in database outages?" from a Python script returns a grounded, sourced answer.

---

## Day 5 — API and frontend

- [ ] Write `api/main.py` — FastAPI `/query` endpoint
- [ ] Test endpoint with Postman or curl
- [ ] Write `ui/app.py` — Streamlit frontend with text input and filter dropdowns
- [ ] Connect frontend to backend
- [ ] Do a full end-to-end test

**Done when:** you can type a question in the browser and get an answer with sources shown below.

---

## Day 6 — Polish and deploy

- [ ] Write `README.md` with project description, setup steps, and screenshot
- [ ] Push to GitHub
- [ ] Deploy FastAPI backend on Render
- [ ] Deploy Streamlit frontend on Streamlit Cloud
- [ ] Test the live deployed version
- [ ] Write and publish LinkedIn post

**Done when:** live link works, GitHub repo is public, LinkedIn post is up.

---

## If you fall behind

- Skip Streamlit on day 5 — a working terminal demo is enough for day 6 screenshots
- Reduce corpus to 10 docs if ingestion is taking too long
- Use a hardcoded metadata dict instead of auto-extraction if tagging is slow

---

## v2 ideas (after you ship)

- Auto-extract metadata with an LLM during ingestion
- Add BM25 keyword search alongside vector search (true hybrid retrieval)
- Swap ChromaDB for Pinecone for cloud persistence
- Add a "similar incidents" feature — given a new incident description, find the closest postmortems