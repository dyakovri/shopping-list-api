FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements*.txt /app/
RUN pip install -r /app/requirements.txt -r /app/requirements.dev.txt

COPY . /app
