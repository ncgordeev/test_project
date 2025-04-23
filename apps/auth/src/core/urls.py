from django.urls import include, path

urlpatterns = [
    path("", include("apps.users.urls", namespace="users")),
]
