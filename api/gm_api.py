from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from core.gm_agent import init_agent, ask_gm_stream
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_agent()  # runs on startup
    yield
    # anything after yield runs on shutdown

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask(request: QueryRequest):
    return StreamingResponse(
        ask_gm_stream(request.query),
        media_type="text/plain"
    )

@app.get("/health")
async def health():
    return {"status": "Veildark Game Master is alive"}


