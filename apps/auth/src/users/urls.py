from django.urls import path

from .apps import UsersConfig
from .views import AuthView, SigninView, SignupView

app_name = UsersConfig.name
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("auth/", AuthView.as_view(), name="auth"),
]
