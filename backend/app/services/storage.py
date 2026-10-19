import io
from minio import Minio
from minio.error import S3Error
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except Exception as e:
            # Ghi log nhưng không làm crash nếu MinIO chưa sẵn sàng lúc build
            print(f"[StorageService] Warning: Could not connect to MinIO: {e}")

    def upload_file(self, object_name: str, file_data: bytes, content_type: str = "application/pdf") -> str:
        """Tải file lên MinIO S3 bucket và trả về s3_key"""
        try:
            data_stream = io.BytesIO(file_data)
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=len(file_data),
                content_type=content_type
            )
            return f"{self.bucket_name}/{object_name}"
        except S3Error as err:
            raise RuntimeError(f"Lỗi khi upload file lên MinIO: {err}")

    def get_presigned_url(self, object_name: str, expires_seconds: int = 3600) -> str:
        """Sinh Pre-signed URL cho phép trình duyệt truy cập file trực tiếp"""
        try:
            # Xóa tiền tố bucket_name nếu có
            clean_name = object_name.replace(f"{self.bucket_name}/", "")
            return self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=clean_name,
                expires=expires_seconds
            )
        except Exception as err:
            # Fallback URL
            return f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{clean_name}"

storage_service = StorageService()
