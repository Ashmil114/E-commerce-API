from django.urls import path
from .views import (
    test,
    login_with_otp,
    validate_otp,
    logout,
    user,
    create_address,
    address_update_delete,
    address_list,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("ping", test.as_view()),
    path("verification-code", login_with_otp.as_view()),
    path("validate-verification-code", validate_otp.as_view()),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", logout.as_view()),
    path("user", user.as_view()),
    path("add-address", create_address.as_view()),
    path("address", address_list.as_view()),
    path("address/<pk>", address_update_delete.as_view()),
]
