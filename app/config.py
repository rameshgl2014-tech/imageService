# import os

# AWS_REGION = "us-east-1"
# S3_BUCKET = "image-bucket"
# DYNAMO_TABLE = "images"
#
# ENDPOINT_URL = "http://localhost:4566"


import os

ENDPOINT_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "image-bucket")
DYNAMO_TABLE = "Images"

