from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk


class DocumentService:

    def create_document(
        self,
        db: Session,
        title: str,
        source: str,
        document_metadata: dict | None = None,
    ) -> Document:
        document = Document(
            title=title,
            source=source,
            document_metadata=document_metadata,
        )

        db.add(document)
        db.flush()

        return document

    def add_chunk(
        self,
        db: Session,
        document_id: int,
        content: str,
        chunk_index: int,
        embedding: list[float],
    ) -> DocumentChunk:
        chunk = DocumentChunk(
            document_id=document_id,
            content=content,
            chunk_index=chunk_index,
            embedding=embedding,
        )

        db.add(chunk)

        return chunk


document_service = DocumentService()