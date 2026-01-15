#!/bin/bash
set -e

echo "Creating S3 bucket..."
awslocal s3 mb s3://image-bucket || true

echo "Creating DynamoDB table..."
awslocal dynamodb create-table \
  --table-name Images \
  --attribute-definitions AttributeName=image_id,AttributeType=S \
  --key-schema AttributeName=image_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST || true
