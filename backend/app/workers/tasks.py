from app.workers.celery_app import celery_app
from app.services.ingestion_service import ingestion_service


@celery_app.task
def process_document(file_path: str):
    document_id = ingestion_service.ingest(file_path)

    return {
        "status": "processed",
        "document_id": document_id,
        "file_path": file_path,
    }