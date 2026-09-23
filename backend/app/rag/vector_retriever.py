from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk
from app.rag.metadata_filter import apply_metadata_filters
from app.schemas.retrieval import RetrievalFilters
from app.services.embedding_service import embedding_service


class VectorRetriever:
    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 10,
        filters: RetrievalFilters | None = None,
    ) -> list[dict]:
        query_embedding = embedding_service.embed_query(query)

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.content,
                DocumentChunk.chunk_index,
                distance.label("distance"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(DocumentChunk.embedding.is_not(None))
        )

        statement = apply_metadata_filters(
            statement,
            filters,
        )

        statement = (
            statement
            .order_by(distance)
            .limit(top_k)
        )

        rows = db.execute(statement).all()

        return [
            {
                "chunk_id": row.id,
                "document_id": row.document_id,
                "content": row.content,
                "chunk_index": row.chunk_index,
                "score": 1 - row.distance,
            }
            for row in rows
        ]


vector_retriever = VectorRetriever()