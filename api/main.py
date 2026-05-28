import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from retrieval.chain import ask

load_dotenv()

app = FastAPI(
    title="FailWise API",
    description="Query engineering postmortems using natural language",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str
    filters: dict = None

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
def root():
    return {"message": "FailWise API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = ask(request.question, request.filters)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))