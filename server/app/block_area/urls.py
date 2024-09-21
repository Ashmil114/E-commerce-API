from django.urls import path
from .views import test, check_block_area

urlpatterns = [
    path("ping", test.as_view()),
    path("", check_block_area.as_view()),
]
