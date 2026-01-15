import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from app.config import ENDPOINT_URL, AWS_REGION, DYNAMO_TABLE


def get_dynamodb_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    return dynamodb.Table(DYNAMO_TABLE)


def save_metadata(item: dict):
    table = get_dynamodb_table()
    table.put_item(Item=item)


def list_images_basic(filters=None):
    table = get_dynamodb_table()
    items = []
    try:
        response = table.scan()
        items.extend(response.get("Items", []))

        # Handle pagination
        while "LastEvaluatedKey" in response:
            response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            items.extend(response.get("Items", []))

    except ClientError as e:
        raise RuntimeError(f"DynamoDB scan failed: {e}")

    return items

def list_images(filters=None):
    table = get_dynamodb_table()

    scan_kwargs = {}
    filter_expr = None

    if filters:
        if filters.get("user"):
            filter_expr = Attr("user").eq(filters["user"])

        if filters.get("tag"):
            tag_expr = Attr("tag").eq(filters["tag"])
            filter_expr = tag_expr if not filter_expr else filter_expr & tag_expr

        if filter_expr:
            scan_kwargs["FilterExpression"] = filter_expr

    response = table.scan(**scan_kwargs)
    items = response.get("Items", [])

    # Handle pagination
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            **scan_kwargs
        )
        items.extend(response.get("Items", []))

    return items


def delete_metadata(image_id: str):
    table = get_dynamodb_table()
    table.delete_item(Key={"image_id": image_id})
