#!/bin/bash

set -e

if ! command -v ruff &> /dev/null; then
  echo "ruff не установлен"
  exit 1
fi

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Запуск линтера..."
ruff check --fix "$PROJECT_DIR" || { echo "Ошибка"; exit 1; }

echo ""

echo "Запуск форматирования кода..."
ruff format "$PROJECT_DIR"  || { echo "Ошибка"; exit 1; }

echo "Готово!"
