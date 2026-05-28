FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

RUN pip install --no-cache-dir .

CMD ["uvicorn", "org_struct.main:app", "--host", "0.0.0.0", "--port", "8000"]
