import uuid
import base64
from app.services.s3_service import upload_image
from app.services.dynamo_service import save_metadata
from app.utils.response import response
from app.utils.logger import get_logger
import json
logger = get_logger(__name__)

def handler(event, context):
    try:
        body = json.loads(event["body"])   # ✅ FIX HERE

        image_bytes = base64.b64decode(body["image"])
        image_id = str(uuid.uuid4())

        upload_image(image_id, image_bytes)

        save_metadata({
            "image_id": image_id,
            "user": body.get("user"),
            "tag": body.get("tag")
        })

        return {
            "statusCode": 201,
            "body": json.dumps({"image_id": image_id})
        }

    except Exception as e:
        logger.exception("Image Uploading failed reason : %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



