from django.urls import path
from .views import test

urlpatterns = [
    path("ping", test.as_view()),
]
