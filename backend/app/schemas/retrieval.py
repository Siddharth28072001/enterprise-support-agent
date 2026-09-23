from pydantic import BaseModel, Field


class RetrievalFilters(BaseModel):
    category: str | None = None
    document_type: str | None = None
    department: str | None = None
    source_type: str | None = None


class RetrievalRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
    )

    top_k: int = Field(
        default=10,
        ge=1,
        le=50,
    )

    filters: RetrievalFilters | None = None


class RetrievedChunk(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    chunk_index: int
    score: float


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievedChunk]