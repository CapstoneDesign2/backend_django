from django.urls import path, include
from .views import helloAPI, randomQuiz, cafeAPI, gradeCafe

urlpatterns = [
    path("hello/",helloAPI), 
    path("<int:id>/",randomQuiz),
    path("cafe/",cafeAPI),
    path("gcafe",gradeCafe),
]