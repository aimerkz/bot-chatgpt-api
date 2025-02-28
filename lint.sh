#!/bin/bash

set -e

if ! command -v ruff &> /dev/null; then
  echo "ruff не установлен"
  exit 1
fi

echo "Запуск линтера..."
ruff check --fix || { echo "Ошибка"; exit 1; }

echo ""

echo "Запуск форматирования кода..."
ruff format .

echo "Готово!"
