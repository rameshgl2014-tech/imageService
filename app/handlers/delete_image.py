from app.services.s3_service import delete_image
from app.services.dynamo_service import delete_metadata


def handler(event, context):
    image_id = event["pathParameters"]["image_id"]  # ✅ FIX

    delete_image(image_id)
    delete_metadata(image_id)

    return {
        "statusCode": 200,
        "body": f'{{"deleted": "{image_id}"}}'
    }
