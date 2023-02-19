FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY test_app.py .

CMD ["python", "test_app.py", "172.17.0.1"]
