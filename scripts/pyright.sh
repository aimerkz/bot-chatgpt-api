#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v pyright &> /dev/null; then
  echo "pyright не установлен"
  exit 1
fi

echo "Запуск проверки типов..."
pyright -p "$PROJECT_DIR"/pyproject.toml || { echo "Ошибка"; exit 1; }

echo "Готово!"