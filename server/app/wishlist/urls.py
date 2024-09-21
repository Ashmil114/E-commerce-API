from django.urls import path
from .views import (
    test,
    wishlist_list,
    create_wishlists,
    wishlist_item_view,
    wishlist_update_delete,
)

urlpatterns = [
    path("ping", test.as_view()),
    path("", wishlist_list.as_view()),
    path("add", create_wishlists.as_view()),
    path("item", wishlist_item_view.as_view()),
    path("<pk>", wishlist_update_delete.as_view()),
]
