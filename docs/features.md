# FailWise — Features

## Core features

### Section-aware ingestion
Postmortems are not chunked by arbitrary token windows. Each document is split
by incident section — timeline, root cause, resolution, and learnings — so every
chunk retrieved has a single clear purpose.

### Structured metadata tagging
Every chunk carries structured metadata:
- `company` — e.g. Cloudflare, AWS, Stripe
- `year` — year of the incident
- `severity` — P0, P1, P2
- `category` — e.g. DNS failure, database outage, network partition
- `chunk_type` — timeline / root_cause / resolution / learnings

### Hybrid retrieval
Queries are resolved in two stages:
1. Metadata filters applied first as hard constraints
2. Semantic similarity search over the filtered subset

This means "Cloudflare DNS incidents from 2023" applies company and category as
exact filters before any vector search runs — not everything is left to cosine
similarity.

### Grounded answers with source attribution
Every answer references the postmortem it came from. The system prompt explicitly
instructs the model to answer only from retrieved context and never fabricate.
Sources are shown below each answer in the UI.

### Natural language querying
Ask questions the way you would ask a senior engineer:
- "What monitoring gaps appear most in database outages?"
- "How did teams handle cascading failures?"
- "What changed after the Cloudflare BGP incident?"
- "Summarise all P0 incidents involving DNS"

### Filter-assisted search
The Streamlit UI exposes optional dropdowns for company and category so users
can narrow the search space before asking a question. Filters are passed directly
to the retrieval layer as metadata constraints.

### REST API
A FastAPI `/query` endpoint exposes the retrieval chain programmatically.
Accepts a question and optional filters, returns an answer and source list.
Useful for integration or future frontend swaps.

---

## What FailWise does not do

- It does not access the internet or fetch live incident data at query time
- It does not diagnose or predict incidents in your own infrastructure
- It does not guarantee accuracy — always verify against the original postmortem
- It is not a replacement for a proper incident management tool

---

## Planned v2 features

- [ ] Auto-extract metadata with an LLM during ingestion instead of manual tagging
- [ ] BM25 keyword search alongside vector search for true hybrid retrieval
- [ ] "Similar incidents" mode — paste a new incident description, get closest postmortems
- [ ] Postmortem template generator — given a category, generate a structured draft
- [ ] Swap ChromaDB for Pinecone for cloud-native persistence
- [ ] Slack bot interface