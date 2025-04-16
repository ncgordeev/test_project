#!/usr/bin/env python
"""
Утилита для запуска тестов с использованием testcontainers
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

from testcontainers.mongodb import MongoDbContainer


def main():
    parser = argparse.ArgumentParser(description="Запуск тестов с testcontainers")
    parser.add_argument("--e2e", action="store_true", help="Запустить только e2e тесты")
    parser.add_argument("--unit", action="store_true", help="Запустить только unit тесты")
    parser.add_argument("--host", default="0.0.0.0", help="Хост для приложения")
    parser.add_argument("--port", default="8000", help="Порт для приложения")
    args = parser.parse_args()

    # Устанавливаем переменную среды для настроек Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")

    # Устанавливаем переменные окружения для тестового режима
    os.environ["DEBUG"] = "True"
    os.environ["SECRET_KEY"] = "test-secret-key-for-pytest"
    os.environ["DJANGO_ALLOWED_HOSTS"] = "localhost,127.0.0.1,0.0.0.0"

    # Формируем команду pytest
    pytest_args = ["-v"]

    if args.e2e:
        pytest_args.append("-m")
        pytest_args.append("e2e")
    elif args.unit:
        pytest_args.append("-m")
        pytest_args.append("not e2e")

    # Запускаем MongoDB в контейнере
    print("Запуск MongoDB в контейнере...")
    with MongoDbContainer("mongo:latest") as mongo:
        # Устанавливаем переменные окружения
        os.environ["MONGODB_URI"] = mongo.get_connection_url()
        os.environ["TEST_HOST"] = args.host
        os.environ["TEST_PORT"] = args.port

        print(f"MongoDB запущена по адресу: {mongo.get_connection_url()}")
        print(f"Запуск тестов с параметрами: pytest {' '.join(pytest_args)}")

        # Добавляем текущий каталог в переменную PYTHONPATH
        current_path = str(Path.cwd())
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] = f"{current_path}:{os.environ['PYTHONPATH']}"
        else:
            os.environ["PYTHONPATH"] = current_path

        # Запускаем тесты
        result = subprocess.run(["pytest"] + pytest_args, env=os.environ)

        # Возвращаем статус выполнения
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()