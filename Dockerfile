FROM python:3.12-slim

WORKDIR /src
COPY . /src

ENV DB_URL=postgresql+asyncpg://postgres:kDshu3E5QpE0geqd9hS3m232hS9OQJ@138.124.114.106:5432/postgres

RUN pip install -r requirements.txt
RUN alembic init -t async migration
RUN alembic upgrade head

EXPOSE 8000

WORKDIR /src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]