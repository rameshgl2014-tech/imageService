from app.handlers.list_images import handler

def test_list_images():
    response = handler({"queryStringParameters": None}, None)
    assert response["statusCode"] == 200
