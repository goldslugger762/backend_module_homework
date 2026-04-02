from sqlalchemy import text

from core.database import SessionLocal


class HealthService:
    def __init__(self):
        pass

    async def check_db_connection(self) -> bool:
        async with SessionLocal() as db:
            try:
                result = await db.execute(text("SELECT 1"))
                result.fetchone()
                return True
            except Exception as e:
                print("DB health check error:", e)
                return False

    async def check_minio_connection(
        self,
        s3_url: str,
        s3_access_key: str,
        s3_secret_key: str,
        s3_region: str
    ) -> bool:
        import aioboto3
        from botocore.config import Config

        session = aioboto3.Session(
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            region_name=s3_region,
        )

        try:
            async with session.client(
                "s3",
                endpoint_url=s3_url,
                config=Config(signature_version="s3v4"),
            ) as client:
                await client.list_buckets()
                return True
        except Exception as e:
            print("MinIO health check error:", e)
            return False