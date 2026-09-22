from pathlib import Path

from app.database import SessionLocal
from app.services.chunking_service import chunking_service
from app.services.document_service import document_service
from app.services.embedding_service import embedding_service
from app.services.pdf_service import pdf_service


class IngestionService:

    def ingest(self, file_path: str) -> int:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        # 1. Extract text
        text = pdf_service.extract_text(file_path)

        if not text.strip():
            raise ValueError(
                f"No text could be extracted from: {file_path}"
            )

        # 2. Split text into chunks
        chunks = chunking_service.split_text(text)

        if not chunks:
            raise ValueError(
                f"No chunks were generated from: {file_path}"
            )

        db = SessionLocal()

        try:
            # 3. Create document record
            document = document_service.create_document(
                db=db,
                title=path.stem,
                source=str(path),
            )

            # 4. Generate embeddings and save chunks
            for index, chunk in enumerate(chunks):
                embedding = embedding_service.embed_document(
                    chunk
                )

                document_service.add_chunk(
                    db=db,
                    document_id=document.id,
                    content=chunk,
                    chunk_index=index,
                    embedding=embedding,
                )

            # 5. Commit everything as one transaction
            db.commit()

            return document.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


ingestion_service = IngestionService()