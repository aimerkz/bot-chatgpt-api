FROM python:3.12-alpine

ARG APP_DIR=/src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_PATH=$APP_DIR \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PATH=$APP_DIR/.venv/bin:/root/.local/bin:$PATH

WORKDIR $APP_DIR
COPY pyproject.toml uv.lock $APP_DIR

RUN apk add --no-cache curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv sync --no-dev --no-install-project -n -q

COPY . $APP_DIR
CMD ["uv", "run", "app/bot.py"]
