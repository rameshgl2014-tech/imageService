import boto3
from botocore.exceptions import ClientError
from app.config import ENDPOINT_URL, AWS_REGION, S3_BUCKET


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )


def upload_image(key, data):
    s3 = get_s3_client()
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)


def get_image(key):
    s3 = get_s3_client()
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return obj["Body"].read()
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise


def delete_image(key):
    s3 = get_s3_client()
    s3.delete_object(Bucket=S3_BUCKET, Key=key)
