# FROM python:3.10.8-slim as python-base
FROM tiangolo/uvicorn-gunicorn:python3.11

COPY ./app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
CMD ["fastapi", "run", "/app/app.py", "--port", "8888"]
