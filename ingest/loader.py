import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(data_path: str) -> list:
    loader = DirectoryLoader(
        data_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    return documents

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "postmortems")
    
    docs = load_documents(data_path)
    print(f"Loaded {len(docs)} documents")
    print(docs[0].page_content[:200])