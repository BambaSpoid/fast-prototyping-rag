from fastapi import FastAPI
from rag.api.routes import rag as rag_routes

app = FastAPI(title="Elastic RAG API")
app.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])


@app.get("/")
def root():
    return {"ok": True}
