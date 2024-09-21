from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rest_framework import generics

from django_filters import rest_framework as filters
from .pagination import Pagination

from .filter_set import ProductFilter, SubCategoryFilter

from .models import tb_product, tb_product_subcategory
from .serializers import product_serializer, product_subcategory_serializers


class test(APIView):
    def get(self, request):
        return Response("product test ping")


class product_list(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_product.objects.all()
    serializer_class = product_serializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Pagination
    # def get_queryset(self):
    #     return tb_product.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class product_detail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_product.objects.all()
    serializer_class = product_serializer


class sub_category_list(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_product_subcategory.objects.all()
    serializer_class = product_subcategory_serializers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubCategoryFilter

    def get_queryset(self):
        return tb_product_subcategory.objects.filter(products__isnull=False).distinct()
