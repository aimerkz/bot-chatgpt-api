#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v pytest &> /dev/null; then
  echo "pytest не установлен"
  exit 1
fi

echo "Запуск тестов..."
pytest -v -s -c "$PROJECT_DIR"/pyproject.toml "$PROJECT_DIR"/tests/ || { echo "Ошибка"; exit 1; }

echo "Готово!"
