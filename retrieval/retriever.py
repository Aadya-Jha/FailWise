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