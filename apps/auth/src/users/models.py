import bcrypt
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.
    """

    def create_user(self, email: str, password: str, **extra_fields: dict) -> "User":
        """
        Метод создания нового пользователя.
        """
        if not email:
            raise ValueError("Поле email обязательно для заполнения.")

        email = self.normalize_email(email)
        password = self.normalize_password(password)
        extra_fields.pop("username", None)

        user = self.model(email=email, password_hash=password, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        """
        Метод создания суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        extra_fields.pop("username", None)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    ROLES = (
        ("user", "Пользователь"),
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
    )
    username = None
    name = models.CharField(max_length=30, verbose_name="Имя")
    role = models.CharField(
        max_length=50, choices=ROLES, verbose_name="Роль", default="user"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    password_hash = models.CharField(max_length=128, verbose_name="Пароль")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def set_password(self, password: str) -> None:
        """
        Метод для хеширования пароля.
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    def __str__(self):
        return self.email
