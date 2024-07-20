from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client
from types_aiobotocore_s3.type_defs import BlobTypeDef

from likulau.env import env

session = get_session()


def s3_client():
    return session.create_client(
        "s3",
        endpoint_url=env("S3_ENDPOINT"),
        aws_secret_access_key=env("S3_ACCESS_KEY"),
        aws_access_key_id=env("S3_KEY_ID"),
    )


async def upload_file(key: str, body: BlobTypeDef):
    async with s3_client() as client:
        client: S3Client
        await client.put_object(Bucket=env("BUCKET_NAME"), Key=key, Body=body)
