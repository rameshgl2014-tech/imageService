import json, base64
from app.handlers.upload import handler

def test_upload():
    event = {
        "body": json.dumps({
            "image": base64.b64encode(b"pytest-image").decode(),
            "user": "tester",
            "tag": "pytest"
        })
    }

    response = handler(event, None)

    assert response["statusCode"] == 201
