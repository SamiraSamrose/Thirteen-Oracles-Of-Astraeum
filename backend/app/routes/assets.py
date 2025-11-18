### File: backend/app/routes/assets.py

"""
backend/app/routes/assets.py
STEP: Asset Management API Routes
Handles MinIO asset uploads, downloads, signed URLs.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.services.storage_service import StorageService

router = APIRouter()
storage_service = StorageService()


@router.post("/upload")
async def upload_asset(
    file: UploadFile = File(...),
    path: str = "assets/"
):
    """
    Upload asset to MinIO.
    STEP: Stores file in object storage, returns path.
    """
    file_path = f"{path}{file.filename}"
    
    try:
        await storage_service.upload_file(
            file_path,
            file.file,
            file.content_type or "application/octet-stream"
        )
        
        return {
            "message": "File uploaded successfully",
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_path:path}")
async def download_asset(file_path: str):
    """
    Download asset from MinIO.
    STEP: Retrieves file data and streams to client.
    """
    try:
        file_data = await storage_service.download_file(file_path)
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/url/{file_path:path}")
async def get_presigned_url(file_path: str):
    """
    Get presigned URL for asset.
    STEP: Generates temporary signed URL for frontend access.
    """
    try:
        url = await storage_service.get_presigned_url(file_path)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
