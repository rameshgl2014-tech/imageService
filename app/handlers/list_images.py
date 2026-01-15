from app.services.dynamo_service import list_images
from app.utils.response import response


def handler(event, context):
    """
    GET /images?user=x&tag=y
    List images with optional filters
    """

    # Query parameters from API Gateway
    filters = event.get("queryStringParameters") or {}

    items = list_images(filters)

    return response(200, {
        "count": len(items),
        "images": items
    })
