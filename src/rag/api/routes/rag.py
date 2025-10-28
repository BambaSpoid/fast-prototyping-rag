from fastapi import APIRouter, Query
from rag.core.retrieval import search_bm25
from rag.core.generator import summarize_incidents

router = APIRouter()


@router.get("/search")
def search(q: str = Query(..., min_length=2), k: int = 5):
    results = search_bm25(q, k)
    return {"query": q, "results": results}


@router.get("/ask")
def ask(q: str = Query(..., min_length=2), k: int = 5):
    incidents = search_bm25(q, k)
    summary = summarize_incidents(q, incidents)
    return {
        "query": q,
        "answer": summary,
        "raw": incidents,
    }
