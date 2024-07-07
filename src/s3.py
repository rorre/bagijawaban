from aiobotocore.session import get_session

from likulau.env import env

session = get_session()


def s3_client():
    return session.create_client(
        "s3",
        endpoint_url=env("S3_ENDPOINT"),
        aws_secret_access_key=env("S3_ACCESS_KEY"),
        aws_access_key_id=env("S3_KEY_ID"),
    )
