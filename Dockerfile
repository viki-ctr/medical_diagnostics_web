FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.6.1
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
