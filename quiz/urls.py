from django.urls import path, include
from .views import cafeAPI, helloAPI, reviewAPI, signupTestAPI, cafeLocationAPI

urlpatterns = [
    path("hello/",helloAPI),
    path("cafe/",cafeAPI),
    path("review/",reviewAPI),
    path("test/",signupTestAPI),
    path("location/",cafeLocationAPI)
]