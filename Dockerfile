FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# 🔑 Make imports like `from app.services...` work
ENV PYTHONPATH=/app

ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_DEFAULT_REGION=us-east-1
ENV LOCALSTACK_ENDPOINT=http://localstack:4566

#CMD ["tail", "-f", "/dev/null"]
CMD ["python", "-m", "app.api"]
