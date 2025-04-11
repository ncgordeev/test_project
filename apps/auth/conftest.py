from datetime import datetime

import bcrypt
import pytest
from django.core.cache import cache
from django.test import Client
from src.users.utils import get_db_handle, users_collection
from testcontainers.mongodb import MongoDbContainer

# fmt: off
pytest_plugins = [
]


# fmt: on


@pytest.fixture(autouse=True)
def _cache():
    """Очистка кеша Django"""
    yield
    cache.clear()


@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo


@pytest.fixture(scope="function", autouse=True)
def clear_db(mongo_container):
    # Получаем подключение к тестовой БД
    db, client = get_db_handle()
    db.users.delete_many({})
    yield
    db.users.delete_many({})
    client.close()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user():
    hashed_pw = bcrypt.hashpw(b"test_password", bcrypt.gensalt()).decode()

    user_data = {
        "email": "test_user@example.com",
        "password": hashed_pw,
        "created_at": datetime.now(),
    }

    user_id = users_collection.insert_one(user_data).inserted_id

    return {"_id": str(user_id), **user_data}


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()
