from django.urls import path, include
from .views import bookmarkDisableAPI, bookmarkEnableAPI, bookmarkListAPI, cafeAPI, helloAPI, isBookmarkAPI, orderByBookmarkAPI, recommendAPI, reviewAPI, cafeLocationAPI

urlpatterns = [
    path("hello/",helloAPI),
    path("cafe/",cafeAPI),
    path("review/",reviewAPI),
    path("location/",cafeLocationAPI),
    path("cafe/bookmark/enable",bookmarkEnableAPI),
    path("cafe/bookmark/disable",bookmarkDisableAPI),
    path("cafe/bookmark/is",isBookmarkAPI),
    path("cafe/bookmark/list",bookmarkListAPI),
    path("cafe/bookmark",orderByBookmarkAPI),
    path("cafe/recommend",recommendAPI),
]