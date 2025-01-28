FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_PATH=/src/ \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    PATH="/root/.local/bin:$PATH" \
    PYTHONPATH="/src"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $APP_PATH

COPY pyproject.toml poetry.lock $APP_PATH
RUN poetry install --no-root --without dev

COPY . $APP_PATH
COPY app/.env $APP_PATH

CMD ["poetry", "run", "python3", "app/bot.py"]
