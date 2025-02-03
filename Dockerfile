FROM python:3.12-alpine

ARG APP_DIR=/src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    APP_PATH=$APP_DIR \
    PATH=$APP_DIR/.venv/bin:/root/.local/bin:$PATH

WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock $APP_DIR

RUN apk add --no-cache curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install --no-root --without dev

COPY . $APP_DIR
CMD ["poetry", "run", "python3", "app/bot.py"]
