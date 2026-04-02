import sys

from fastapi import APIRouter, Depends

from services import HealthService
from core.config import settings

router = APIRouter(tags=["system"])


@router.get("/health")
async def health_check(service: HealthService = Depends(HealthService)):
    db_status = await service.check_db_connection()
    minio_status = await service.check_minio_connection(
        s3_url=settings.s3_url,
        s3_access_key=settings.s3_access_key,
        s3_secret_key=settings.s3_secret_key,
        s3_region=settings.s3_region,
    )

    if db_status and minio_status:
        return {"status": "healthy", "db": "ok", "minio": "ok"}

    return {
        "status": "unhealthy",
        "db": "ok" if db_status else "error",
        "minio": "ok" if minio_status else "error",
    }


@router.get("/info")
async def get_info():
    return {
        "version": settings.app_version,
        "environment": settings.environment,
        "python_version": sys.version.split()[0],
    }
