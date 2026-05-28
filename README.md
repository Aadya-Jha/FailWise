# FailWise

FailWise is a retrieval-augmented search system for engineering incident postmortems. It combines metadata-aware filtering with semantic retrieval to answer natural-language questions over real outage reports from Cloudflare, AWS, GitHub, Stripe, and Discord.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-black?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-5A67D8?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

---

## Overview

FailWise indexes public engineering postmortems and enables semantic querying across incident reports.

Example queries:
- *What caused the Cloudflare 2025 outage?*
- *How did GitHub handle database failovers?*
- *What monitoring failures appear most frequently across incidents?*
- *How were cascading failures mitigated during large-scale outages?*

Responses are grounded exclusively in retrieved documents and attributed to their original sources.

---

## System Architecture

1. Markdown postmortems are parsed and segmented by incident section
2. Metadata is attached to each chunk (company, severity, category, incident type)
3. Chunks are embedded using Gemini embeddings
4. Embeddings are persisted in ChromaDB
5. Queries execute through hybrid retrieval — metadata filtering first, semantic vector search second
6. Retrieved context is passed into a Gemini-powered RAG chain
7. Responses are exposed through FastAPI and Streamlit interfaces

---

## Design Decisions

**Section-aware chunking**
Postmortems are segmented by incident section — timeline, root cause, resolution, learnings — rather than fixed token windows. Each chunk preserves a single semantic unit, improving retrieval precision.

**Hybrid retrieval**
Metadata filtering executes before semantic retrieval. Structured constraints such as company, severity, or category narrow the search space before vector similarity ranking runs.

**Retrieval-constrained generation**
The generation layer is restricted to retrieved context from the indexed corpus. When insufficient evidence is available, the system explicitly returns uncertainty rather than generating unsupported responses from model pretraining knowledge.

---

## Repository Structure

```text
failwise/
├── data/
│   └── postmortems/          raw markdown postmortems
├── ingest/
│   ├── loader.py             loads documents from disk
│   ├── chunker.py            section-aware splitting + metadata tagging
│   └── embedder.py           embeds chunks and stores in ChromaDB
├── retrieval/
│   ├── retriever.py          hybrid metadata + semantic retrieval
│   └── chain.py              LangChain RAG chain with Gemini
├── api/
│   └── main.py               FastAPI /query endpoint
├── ui/
│   └── app.py                Streamlit frontend
├── chroma_store/             persisted ChromaDB index
├── docs/
└── requirements.txt
```

---

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/Aadya-Jha/FailWise.git
cd FailWise
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_api_key
```

**5. Run the ingestion pipeline**
```bash
python ingest/embedder.py
```

**6. Start the backend**
```bash
uvicorn api.main:app --reload
```

**7. Launch the frontend**
```bash
streamlit run ui/app.py
```

---

## API

**POST** `/query`

Request:
```json
{
  "question": "What caused the Cloudflare outage?",
  "filters": {
    "company": "Cloudflare"
  }
}
```

Response:
```json
{
  "answer": "The outage was caused by...",
  "sources": ["cloudflare_2025_network_outage.md"]
}
```

Swagger docs at `http://localhost:8000/docs`

---

## Data Sources

Postmortems are sourced from public engineering blogs and the community-maintained [danluu/post-mortems](https://github.com/danluu/post-mortems) repository.

---

## Future Work

- Add BM25-based keyword retrieval alongside vector search
- Automate metadata extraction during ingestion
- Swap ChromaDB for Pinecone for cloud-native persistence
- Add incident similarity search for related outage discovery
- Integrate Slack-based querying for on-call teams

---

## License

MIT