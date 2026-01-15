import json, base64
from app.handlers.upload import handler as upload
from app.handlers.get_image import handler as get_img

def test_get_image():
    upload_res = upload({
        "body": json.dumps({
            "image": base64.b64encode(b"img").decode()
        })
    }, None)

    image_id = json.loads(upload_res["body"])["image_id"]

    res = get_img({
        "pathParameters": {"image_id": image_id}
    }, None)

    assert res["statusCode"] == 200
