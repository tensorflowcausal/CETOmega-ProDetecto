
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r ValidationPkg/docs/requirements.txt
CMD ["python", "run_validation.py"]
