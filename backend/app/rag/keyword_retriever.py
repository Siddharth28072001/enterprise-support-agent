from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk
from app.rag.metadata_filter import apply_metadata_filters
from app.schemas.retrieval import RetrievalFilters


class KeywordRetriever:
    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 10,
        filters: RetrievalFilters | None = None,
    ) -> list[dict]:
        ts_query = func.websearch_to_tsquery(
            "english",
            query,
        )

        rank = func.ts_rank_cd(
            DocumentChunk.content_tsv,
            ts_query,
        )

        statement = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.content,
                DocumentChunk.chunk_index,
                rank.label("score"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(
                DocumentChunk.content_tsv.op("@@")(ts_query)
            )
        )

        statement = apply_metadata_filters(
            statement,
            filters,
        )

        statement = (
            statement
            .order_by(desc(rank))
            .limit(top_k)
        )

        rows = db.execute(statement).all()

        return [
            {
                "chunk_id": row.id,
                "document_id": row.document_id,
                "content": row.content,
                "chunk_index": row.chunk_index,
                "score": float(row.score),
            }
            for row in rows
        ]


keyword_retriever = KeywordRetriever()