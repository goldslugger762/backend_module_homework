from io import BytesIO

from botocore.exceptions import ClientError, BotoCoreError
from fastapi import HTTPException

from adapters.storage.base import StorageAdapter
import aioboto3


class S3StorageAdapter(StorageAdapter):
    def __init__(
        self,
        bucket: str,
        url: str,
        access_key: str,
        secret_key: str,
        region: str
    ):
        self.bucket = bucket
        self.url = url
        self.session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    async def upload(self, content: bytes, key: str, content_type: str) -> str:
        try:
            async with self.session.client("s3", endpoint_url=self.url) as client:
                await client.upload_fileobj(
                    BytesIO(content),
                    self.bucket,
                    key,
                    ExtraArgs={"ContentType": content_type},
                )
        except (ClientError, BotoCoreError) as e:
            raise HTTPException(status_code=502, detail=str(e))

        return f"{self.url}/{self.bucket}/{key}"
