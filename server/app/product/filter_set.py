from django_filters import rest_framework as filters
from django.db.models import Q
from .models import tb_product, tb_product_subcategory


class ProductFilter(filters.FilterSet):
    pincode = filters.CharFilter(field_name="seller__pincode")
    district = filters.CharFilter(
        field_name="seller__district", lookup_expr="icontains"
    )
    category = filters.CharFilter(
        field_name="sub_category__title", lookup_expr="icontains"
    )
    search = filters.CharFilter(method="filter_by_all_fields")

    class Meta:
        model = tb_product
        fields = [
            "pincode",
            "district",
            "category",
            "search",
        ]

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(sub_category__title__icontains=value)
        )


class SubCategoryFilter(filters.FilterSet):
    district = filters.CharFilter(
        field_name="products__seller__district", lookup_expr="icontains"
    )

    class Meta:
        model = tb_product_subcategory
        fields = ["district"]
