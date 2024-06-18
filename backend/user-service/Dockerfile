FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN mkdir -p /workspace/app

COPY requirements.txt /workspace/app

RUN pip install --no-cache-dir --upgrade -r /workspace/app/requirements.txt

COPY ./app /workspace/app

WORKDIR /workspace

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
