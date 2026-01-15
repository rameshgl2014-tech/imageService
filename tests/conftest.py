import pytest
import time
import boto3
from botocore.exceptions import ClientError
from app.config import ENDPOINT_URL, AWS_REGION, DYNAMO_TABLE


@pytest.fixture(scope="session", autouse=True)
def create_dynamodb_table():
    dynamodb = boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    # ⏳ Wait until DynamoDB is actually ready
    for _ in range(10):
        try:
            dynamodb.list_tables()
            break
        except Exception:
            time.sleep(2)
    else:
        raise RuntimeError("DynamoDB not ready in LocalStack")

    # ✅ Create table if missing
    tables = dynamodb.list_tables()["TableNames"]

    if DYNAMO_TABLE not in tables:
        dynamodb.create_table(
            TableName=DYNAMO_TABLE,
            AttributeDefinitions=[
                {"AttributeName": "image_id", "AttributeType": "S"}
            ],
            KeySchema=[
                {"AttributeName": "image_id", "KeyType": "HASH"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        dynamodb.get_waiter("table_exists").wait(TableName=DYNAMO_TABLE)
