from flask import Flask, request, jsonify, Response
import json
import base64

from app.handlers.upload import handler as upload_handler
from app.handlers.list_images import handler as list_handler
from app.handlers.get_image import handler as get_handler
from app.handlers.delete_image import handler as delete_handler

app = Flask(__name__)


# -----------------------------
# Upload Image
# POST /images
# -----------------------------
@app.route("/images", methods=["POST"])
def upload_image():
    event = {
        "body": json.dumps(request.json)
    }

    response = upload_handler(event, None)

    return Response(
        response["body"],
        status=response["statusCode"],
        mimetype="application/json"
    )


# -----------------------------
# List Images
# GET /images
# -----------------------------
@app.route("/images", methods=["GET"])
def list_images():
    event = {
        "queryStringParameters": request.args.to_dict() or None
    }

    response = list_handler(event, None)

    return Response(
        response["body"],
        status=response["statusCode"],
        mimetype="application/json"
    )


# -----------------------------
# Get / Download Image
# GET /images/<image_id>
# -----------------------------
@app.route("/images/<image_id>", methods=["GET"])
def get_image(image_id):
    event = {
        "pathParameters": {
            "image_id": image_id
        }
    }

    response = get_handler(event, None)

    # Handler returns base64 image
    image_bytes = base64.b64decode(response["body"])

    return Response(
        image_bytes,
        status=response["statusCode"],
        mimetype="application/octet-stream"
    )


# -----------------------------
# Delete Image
# DELETE /images/<image_id>
# -----------------------------
@app.route("/images/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    event = {
        "pathParameters": {
            "image_id": image_id
        }
    }

    response = delete_handler(event, None)

    return Response(
        response["body"],
        status=response["statusCode"],
        mimetype="application/json"
    )


# -----------------------------
# Health Check
# GET /health
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# -----------------------------
# App Entry Point
# -----------------------------
if __name__ == "__main__":
    # IMPORTANT: host must be 0.0.0.0 for Docker
    app.run(host="0.0.0.0", port=5000, debug=True)
