import os
import pytest
from datetime import datetime
import bcrypt
from django.core.cache import cache
from django.test import Client
from testcontainers.mongodb import MongoDbContainer
from bson import ObjectId

# Установка переменной окружения для Django перед импортом DRF
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Импортируем компоненты Django после настройки DJANGO_SETTINGS_MODULE
from django.conf import settings

from src.users.utils import get_db_handle, users_collection
from rest_framework.test import APIClient

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
def admin_user():
    hashed_pw = bcrypt.hashpw(b"admin_password", bcrypt.gensalt()).decode()

    user_data = {
        "email": "admin@example.com",
        "password": hashed_pw,
        "created_at": datetime.now(),
        "role": "admin"
    }

    user_id = users_collection.insert_one(user_data).inserted_id

    return {"_id": str(user_id), **user_data}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(api_client, test_user):
    """API client with authentication for a regular user"""
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken()
    refresh["user_id"] = test_user["_id"]
    token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def admin_api_client(api_client, admin_user):
    """API client with authentication for an admin user"""
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken()
    refresh["user_id"] = admin_user["_id"]
    token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
