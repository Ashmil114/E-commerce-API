from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # APPS
    path("api/customer/", include("app.customer.urls")),
    path("api/seller/", include("app.seller.urls")),
    path("api/product/", include("app.product.urls")),
    path("api/wishlist/", include("app.wishlist.urls")),
    path("api/order/", include("app.order.urls")),
    path("api/block-area/", include("app.block_area.urls")),
    # DOCUMENTATIONS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
