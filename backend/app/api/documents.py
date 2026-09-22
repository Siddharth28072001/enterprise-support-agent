from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.workers.tasks import process_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    task = process_document.delay(str(file_path))

    return {
        "message": "Document uploaded and ingestion started",
        "filename": file.filename,
        "path": str(file_path),
        "task_id": task.id,
    }