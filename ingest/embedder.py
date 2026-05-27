import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def embed_and_store(chunks: list) -> None:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    persist_dir = os.path.join(base_dir, "chroma_store")

    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Embedding batch {i//batch_size + 1} ({len(batch)} chunks)...")
        
        if i == 0:
            vectorstore = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=persist_dir
            )
        else:
            vectorstore.add_documents(batch)
        
        if i + batch_size < len(chunks):
            print("Waiting 30s for rate limit...")
            time.sleep(30)

    print(f"Successfully embedded {len(chunks)} chunks into ChromaDB")
    print(f"Stored at: {persist_dir}")

if __name__ == "__main__":
    from loader import load_documents
    from chunker import chunk_documents
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs = load_documents(os.path.join(base_dir, "data", "postmortems"))
    chunks = chunk_documents(docs)
    embed_and_store(chunks)