from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from .models import tb_wishlist, tb_wishlist_item
from app.customer.models import tb_customer
from app.product.models import tb_product

from .serializers import wishlist_serializer

from django_filters import rest_framework as filters
from .filter_set import WishlistFilter

from drf_spectacular.utils import extend_schema


class test(APIView):
    def get(self, request):
        return Response("WishList test pong")


class wishlist_list(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_wishlist.objects.all()
    serializer_class = wishlist_serializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WishlistFilter

    def list(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(owner__user=request.user)
        )
        serializer = wishlist_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class create_wishlists(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "district": {"type": "string"},
                },
                "required": ["title", "district"],
            }
        },
        responses=wishlist_serializer,
    )
    def post(self, request):
        title = request.data.get("title")
        district = request.data.get("district")
        try:
            owner = tb_customer.objects.get(user=request.user)
        except tb_customer.DoesNotExist:
            return Response(
                {"error": "Customer Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            tb_wishlist.objects.create(title=title, district=district, owner=owner)
            return Response(
                {"message": "Wishlist Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class wishlist_update_delete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = wishlist_serializer
    queryset = tb_wishlist.objects.all()


class wishlist_item_view(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "wishlist_id": {"type": "string", "format": "uuid"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "format": "uuid"},
                                "quantity": {"type": "number"},
                            },
                            "required": ["id", "quantity"],
                        },
                    },
                },
                "required": ["wishlist_id", "items"],
            }
        },
        responses={
            200: {"type": "object", "properties": {"message": {"type": "string"}}}
        },
    )
    def post(self, request):
        wishlist_id = request.data.get("wishlist_id")
        items_list = request.data.get("items")

        try:
            wishlist = tb_wishlist.objects.get(id=wishlist_id, owner__user=request.user)
        except tb_wishlist.DoesNotExist:
            return Response(
                {"error": "Wishlist Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            for item in items_list:
                product_id = item["id"]
                quantity = str(item["quantity"])
                try:
                    product = tb_product.objects.get(id=product_id)
                except tb_product.DoesNotExist:
                    return Response(
                        {"error": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND
                    )
                if int(quantity) == 0:
                    if wishlist.items.filter(product__title=product.title).exists():
                        item = wishlist.items.filter(product__title=product.title)
                        wishlist.items.remove(item[0])
                        wishlist.save()
                        continue
                    else:
                        continue

                try:
                    wishlist_item = tb_wishlist_item.objects.get(
                        product=product, quantity=quantity
                    )
                except tb_wishlist_item.DoesNotExist:
                    wishlist_item = tb_wishlist_item.objects.create(
                        product=product, quantity=quantity
                    )

                if wishlist.items.filter(product__title=product.title).exists():
                    item = wishlist.items.filter(product__title=product.title)
                    wishlist.items.remove(item[0])
                    wishlist.save()

                try:
                    wishlist.items.add(wishlist_item)
                    wishlist.save()
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                {"message": "Product Added Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
