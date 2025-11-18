### File: backend/app/services/storage_service.py

"""
backend/app/services/storage_service.py
STEP: MinIO/S3 Storage Service
Handles asset storage, retrieval, and signed URL generation for game assets.
"""
from minio import Minio
from minio.error import S3Error
from typing import Optional, BinaryIO
import io

from app.config import settings


class StorageService:
    """MinIO/S3-compatible storage service for game assets"""
    
    def __init__(self):
        """Initialize MinIO client"""
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")
    
    async def upload_file(
        self,
        file_path: str,
        file_data: BinaryIO,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload file to storage.
        STEP: Stores file in MinIO, returns object path.
        """
        try:
            file_size = file_data.seek(0, 2)
            file_data.seek(0)
            
            self.client.put_object(
                self.bucket,
                file_path,
                file_data,
                file_size,
                content_type=content_type
            )
            
            return file_path
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")
    
    async def download_file(self, file_path: str) -> bytes:
        """
        Download file from storage.
        STEP: Retrieves file data from MinIO.
        """
        try:
            response = self.client.get_object(self.bucket, file_path)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Failed to download file: {e}")
    
    async def get_presigned_url(
        self,
        file_path: str,
        expiry_seconds: int = 3600
    ) -> str:
        """
        Generate presigned URL for asset access.
        STEP: Creates temporary signed URL for frontend to fetch assets.
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                file_path,
                expires=timedelta(seconds=expiry_seconds)
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to generate presigned URL: {e}")
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            self.client.remove_object(self.bucket, file_path)
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False
    
    async def list_files(self, prefix: str = "") -> list:
        """List files with given prefix"""
        try:
            objects = self.client.list_objects(self.bucket, prefix=prefix)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"Error listing files: {e}")
            return []
