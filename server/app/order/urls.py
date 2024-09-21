from django.urls import path
from .views import test, orders, order, create_order, update_order_status, cancel_order

urlpatterns = [
    path("ping", test.as_view()),
    path("", orders.as_view()),
    path("<pk>", order.as_view()),
    path("create-order/", create_order.as_view()),
    path("status/<pk>", update_order_status.as_view()),
    path("cancel-order/<pk>", cancel_order.as_view()),
]
