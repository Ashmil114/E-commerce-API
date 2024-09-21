from django.urls import path
from .views import test, product_list, product_detail, sub_category_list

urlpatterns = [
    path("ping", test.as_view()),
    path("", product_list.as_view()),
    path("<pk>", product_detail.as_view()),
    path("sub-category/", sub_category_list.as_view()),
]
