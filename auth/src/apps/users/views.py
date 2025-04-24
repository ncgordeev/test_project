import re
from datetime import datetime

import bcrypt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.settings import ADMIN_SECRET

from .authentication import MongoJWTAuthentication
from .utils import users_collection


class SignupView(APIView):
    """
    Регистрация нового пользователя.
    """

    def post(self, request):
        """
        Регистрирует нового пользователя в базе и возвращает токен доступа.
        :param request: POST запрос с данными email и password
        :return: JSON-ответ с токеном доступа или ошибкой
        """
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            # Проверка наличия email и пароля
            if not email or not password:
                return Response(
                    {"error": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверка правильности ввода email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return Response(
                    {"error": "Invalid email format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверка наличия пользователя с таким email в базе
            if users_collection.find_one({"email": email}):
                return Response(
                    {"error": "User already exists"}, status=status.HTTP_409_CONFLICT
                )

            # Хеширование пароля
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            # Создание пользователя
            role = "user"
            if request.data.get("role") == "admin":
                if request.data.get("admin_secret") != ADMIN_SECRET:
                    return Response({"error": "Invalid admin secret"}, status=403)
                role = "admin"

            user_data = {
                "email": email,
                "password": hashed_pw,
                "created_at": datetime.now(),
                "role": role,
            }

            user = users_collection.insert_one(user_data)
            user_id = str(user.inserted_id)

            # Генерация токена
            refresh = RefreshToken()
            refresh["user_id"] = user_id

            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SigninView(APIView):
    """
    Авторизация пользователя.
    """

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            # Проверка наличия email и пароля
            if not email or not password:
                return Response(
                    {"error": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверка наличия пользователя с таким email в базе
            user = users_collection.find_one({"email": email})
            if not user:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED
                )

            # Проверка пароля
            if not bcrypt.checkpw(
                password.encode("utf8"), user["password"].encode("utf-8")
            ):
                return Response(
                    {"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED
                )

            # Генерация токена
            refresh = RefreshToken()
            refresh["user_id"] = str(user["_id"])

            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )
        except Exception as e:
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AuthView(APIView):
    """
    Проверка авторизации клиента.
    """

    authentication_classes = (MongoJWTAuthentication,)

    def get(self, request):
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return Response(
                    {"error": "Authorization header is missing"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Автоматическая валидация JWTAuthentication
            user = request.user

            # Получаем данные о пользователе из базы
            db_user = users_collection.find_one({"_id": user["_id"]})

            if not db_user:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_403_FORBIDDEN
                )

            response_data = {"message": "Authenticated"}
            response = Response(response_data, status=status.HTTP_200_OK)

            # Добавляем кастомные заголовки
            response["X-USER-ROLE"] = db_user.get("role", "user")
            response["Authorization"] = auth_header

            return response

        except Exception as e:
            return Response(
                {"error": f"Authentication error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
