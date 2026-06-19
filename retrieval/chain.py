import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from retrieval.retriever import load_vectorstore, retrieve_with_document_grouping

load_dotenv()

def format_docs(docs):
    return "\n\n".join([
        f"Source: {doc.metadata.get('source', 'unknown')} | Company: {doc.metadata.get('company', 'unknown')}\n{doc.page_content}"
        for doc in docs
    ])


def ask(question: str, filters: dict = None) -> dict:
    docs = retrieve_with_document_grouping(question, filters)
    
    print(f"Total docs retrieved: {len(docs)}")
    for d in docs[:3]:
        print(d.metadata)
        print(d.page_content[:100])
        print("---")
    
    context = format_docs(docs)
    print(f"Context length: {len(context)}")

    if not docs:
        return {"answer": "I don't have a postmortem for this in my knowledge base.", "sources": []}

    context = format_docs(docs)
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    prompt = PromptTemplate.from_template("""
You are FailWise, an AI assistant that answers questions about engineering incidents and postmortems.

Use ONLY the context below to answer the question.
If the context does not contain enough information, say "I don't have a postmortem for this in my knowledge base" — do not make up an answer.
Always mention which company or incident your answer is based on.

Context:
{context}

Question: {question}

Answer:""")

    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({"context": context, "question": question})
    
    sources = list(set([
        doc.metadata.get("source", "unknown")
        for doc in docs
    ]))

    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    print("=== Test 1: General question ===")
    response = ask("What monitoring gaps appear most often in incidents?")
    print("Answer:", response["answer"])
    print("Sources:", response["sources"])

    print("\n=== Test 2: With filter ===")
    response = ask("How did the team resolve the outage?", filters={"company": "Cloudflare"})
    print("Answer:", response["answer"])
    print("Sources:", response["sources"])