from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешение доступа только администраторам"""

    def has_permission(self, request, view):
        user_role = request.headers.get("X-USER-ROLE")

        if user_role == "admin":
            return True

        return False


class IsUser(BasePermission):
    """Разрешение доступа пользователям"""

    def has_permission(self, request, view):
        user_role = request.headers.get("X-USER-ROLE")

        if user_role == "user" or user_role == "admin":
            return True

        return False
