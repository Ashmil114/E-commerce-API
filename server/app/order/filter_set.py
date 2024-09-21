from django_filters import rest_framework as filters
from .models import tb_order
from django.db.models import Q


class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(method="filter_by_status_fields")

    class Meta:
        model = tb_order
        fields = ["status"]

    def filter_by_status_fields(self, queryset, name, value):
        if value == "processing" or value == "packed":
            return queryset.filter(
                Q(status__icontains="processing") | Q(status__icontains="packed")
            )
        else:
            return queryset.filter(status__icontains=value)
