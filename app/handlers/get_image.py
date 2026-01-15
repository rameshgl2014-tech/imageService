import base64
from app.services.s3_service import get_image


def handler(event, context):
    image_id = event["pathParameters"]["image_id"]  # ✅ FIX

    image_bytes = get_image(image_id)

    return {
        "statusCode": 200,
        "isBase64Encoded": True,
        "body": base64.b64encode(image_bytes).decode()
    }
