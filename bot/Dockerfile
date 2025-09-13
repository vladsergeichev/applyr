FROM python:3.12-slim

ENV PYTHONPATH=.

WORKDIR /opt/applyr_bot

RUN pip install poetry==2.0.0
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-cache --no-ansi

COPY ./app /opt/applyr_bot/app

CMD ["python", "-m", "app.main"]