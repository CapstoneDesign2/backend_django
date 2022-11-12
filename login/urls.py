from django.urls import path, include
from .views import doubleCheckAPI, loginAPI, registerAPI

urlpatterns = [
    path("login/sign_up/double_check",doubleCheckAPI),
    path("login/sign_up/register",registerAPI),
    path("login/login",loginAPI),
]