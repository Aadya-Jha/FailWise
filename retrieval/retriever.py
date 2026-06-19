import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
load_dotenv()

def load_vectorstore() -> Chroma:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    persist_dir = os.path.join(base_dir, "chroma_store")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    return vectorstore

def retrieve(query: str, filters: dict = None, k: int = 5) -> list:
    vectorstore = load_vectorstore()
    
    if filters:
        results = vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filters
        )
    else:
        results = vectorstore.similarity_search(
            query=query,
            k=k
        )
    
    return results

def retrieve_full_incident(query: str, k_candidates: int = 10) -> list:
    vectorstore = load_vectorstore()
    
    # Stage 1: cast a wider net to find the most relevant incident
    candidates = vectorstore.similarity_search_with_score(query, k=k_candidates)
    
    # Tally which incident_id shows up most / scores best
    from collections import Counter
    incident_scores = Counter()
    for doc, score in candidates:
        iid = doc.metadata.get("incident_id")
        incident_scores[iid] += 1  # or sum(1/score) for weighted ranking

    top_incident_id = incident_scores.most_common(1)[0][0]

    # Stage 2: pull EVERY chunk belonging to that one incident
    full_doc_chunks = vectorstore.get(
        where={"incident_id": top_incident_id}
    )
    return full_doc_chunks

def retrieve_with_document_grouping(query: str, filters: dict = None, k: int = 8) -> list:
    vectorstore = load_vectorstore()
    
    if filters:
        results = vectorstore.similarity_search(query=query, k=k, filter=filters)
    else:
        results = vectorstore.similarity_search(query=query, k=k)
    
    # get unique sources from results
    sources = list(set([doc.metadata.get("source") for doc in results]))
    print("Unique sources:", sources)
    
    # fetch all chunks for those sources
    all_chunks = []
    for source in sources:
        source_chunks = vectorstore.similarity_search(
            query=query,
            k=50,
            filter={"source": source}
        )
        all_chunks.extend(source_chunks)
    
    return all_chunks

if __name__ == "__main__":
    print("=== Test 1: No filter ===")
    results = retrieve("What caused the database outage?")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content[:200])
        print(doc.metadata)

    print("\n=== Test 2: Filter by company ===")
    results = retrieve("What monitoring gaps were found?", filters={"company": "Cloudflare"})
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content[:200])
        print(doc.metadata)