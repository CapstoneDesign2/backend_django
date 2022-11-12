from django.urls import path, include
from .views import doubleCheckAPI, loginAPI, registerAPI

urlpatterns = [
    path("sign_up/double_check",doubleCheckAPI),
    path("sign_up/register",registerAPI),
    path("login",loginAPI),
]