from django_filters import rest_framework as filters
from .models import tb_wishlist


class WishlistFilter(filters.FilterSet):
    district = filters.CharFilter(field_name="district", lookup_expr="icontains")

    class Meta:
        model = tb_wishlist
        fields = ["district"]
