import os
from langchain_text_splitters import MarkdownHeaderTextSplitter

def extract_metadata(content: str) -> dict:
    metadata = {}
    for line in content.split("\n"):
        if "**Company:**" in line:
            metadata["company"] = line.split("**Company:**")[-1].strip()
        elif "**Year:**" in line:
            metadata["year"] = line.split("**Year:**")[-1].strip()
        elif "**Severity:**" in line:
            metadata["severity"] = line.split("**Severity:**")[-1].strip()
        elif "**Category:**" in line:
            metadata["category"] = line.split("**Category:**")[-1].strip()
    return metadata

def chunk_documents(documents: list) -> list:
    headers_to_split_on = [
        ("#", "title"),
        ("##", "chunk_type"),
    ]
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )

    all_chunks = []

    for doc in documents:
        frontmatter = extract_metadata(doc.page_content)
        source = os.path.basename(doc.metadata.get("source", "unknown"))

        chunks = splitter.split_text(doc.page_content)

        for chunk in chunks:
            chunk.metadata.update(frontmatter)
            chunk.metadata["source"] = source
            if "chunk_type" in chunk.metadata:
                chunk.metadata["chunk_type"] = chunk.metadata["chunk_type"].lower().replace(" ", "_")
            all_chunks.append(chunk)

    return all_chunks

if __name__ == "__main__":
    from loader import load_documents
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs = load_documents(os.path.join(base_dir, "data", "postmortems"))
    chunks = chunk_documents(docs)
    print(f"Total chunks: {len(chunks)}")
    print("\n--- First chunk content ---")
    print(chunks[0].page_content)
    print("\n--- First chunk metadata ---")
    print(chunks[0].metadata)