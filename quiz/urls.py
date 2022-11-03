from django.urls import path, include
from .views import cafeAPI, helloAPI, reviewAPI

urlpatterns = [
    path("hello/",helloAPI),
    path("cafe/",cafeAPI),
    path("review/",reviewAPI)
]