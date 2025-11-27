from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import storage, csv_processor
from app.models.file_models import FileResponse
from app.utils.validators import validate_csv_file
from fastapi.responses import StreamingResponse
from app.db.mongo import db
import io
from bson import ObjectId

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), id_field: str = None):
    validate_csv_file(file)
    file_id = await storage.save_file(file)
    await csv_processor.process_csv(str(file_id), id_field)
    doc = await storage.get_file_stream(str(file_id))
    return {
        "id": str(file_id),
        "filename": file.filename,
        "status": "processed",
        "records_count": doc[1]["records_count"],
        "fields": doc[1]["fields"]
    }

@router.get("/")
async def list_files():
    cursor = db.files.find().sort("created_at", -1)
    results = []
    async for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "status": doc.get("status"),
            "records_count": doc.get("records_count", 0),
            "fields": doc.get("fields", [])
        })
    return results

@router.get("/{file_id}/download")
async def download_file(file_id: str):
    cursor_doc = await storage.get_file_stream(file_id)
    if not cursor_doc:
        raise HTTPException(404, "File not found")
    stream, doc = cursor_doc
    return StreamingResponse(stream, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={doc['filename']}"})

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    success = await storage.delete_file(file_id)
    if not success:
        raise HTTPException(404, "File not found")
    return {"status": "deleted"}
