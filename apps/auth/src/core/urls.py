from django.urls import include, path

urlpatterns = [
    path("", include("users.urls", namespace="users")),
]
