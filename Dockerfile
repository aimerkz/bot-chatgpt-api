FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    APP_PATH=/src \
    VIRTUALENV=/src/.venv \
    PATH=/src/.venv/bin:/root/.local/bin:$PATH \
    PYTHONPATH=/src

WORKDIR $APP_PATH

RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock $APP_PATH/
RUN poetry install --no-root --without dev

COPY . $APP_PATH/

CMD ["poetry", "run", "python3", "app/bot.py"]
