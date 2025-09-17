FROM python:3.12-slim

WORKDIR /opt/applyr_api

RUN pip install poetry==2.0.0
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-cache --no-ansi

COPY ./app /opt/applyr_api/app
COPY ./tests /opt/applyr_api/tests
COPY alembic.ini /opt/applyr_api/

#CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]