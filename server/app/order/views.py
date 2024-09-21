from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import tb_order, tb_order_item, status_choices
from app.customer.models import tb_customer, tb_address
from app.product.models import tb_product
from .serializers import orders_serializer, order_serializer
from app.block_area.models import tb_block_district, tb_block_pincode

from django_filters import rest_framework as filters
from .filter_set import OrderFilter


class test(APIView):
    def get(self, request):
        return Response("order test ping")


class orders(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_order.objects.all()
    serializer_class = orders_serializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        return tb_order.objects.filter(owner__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class order(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_order.objects.all()
    serializer_class = order_serializer

    def get_queryset(self):
        return tb_order.objects.filter(owner__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class create_order(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "address_id": {"type": "string", "format": "uuid"},
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
                "required": ["address_id", "items"],
            }
        },
        responses={
            201: {"type": "object", "properties": {"message": {"type": "string"}}}
        },
    )
    def post(self, request):
        address_id = request.data.get("address_id")
        items = request.data.get("items")

        if not address_id or not items:
            return Response(
                {"error": "address id or items field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            customer = tb_customer.objects.get(user=request.user)
        except tb_customer.DoesNotExist:
            return Response(
                {"error": "Customer Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            address = tb_address.objects.get(id=address_id, customer__user=request.user)
        except tb_address.DoesNotExist:
            return Response(
                {"error": "Address Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        # Check Order Area is Block or not
        try:
            if tb_block_district.objects.filter(district=address.district).exists():
                return Response(
                    {"error": f"District {address.district} is blocked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except tb_block_district.DoesNotExist:
            pass
        try:
            if tb_block_pincode.objects.filter(pincode=address.pin).exists():
                return Response(
                    {"error": f"Pincode {address.pin} is blocked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except tb_block_district.DoesNotExist:
            pass
        try:

            order = tb_order.objects.create(owner=customer, address=address)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for item in items:

                product_id = item["id"]
                quantity = item["quantity"]
                try:
                    product = tb_product.objects.get(id=product_id)
                except tb_product.DoesNotExist:
                    return Response(
                        {"error": f"Product ID {product_id} Not Found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if quantity <= 0:
                    return Response(
                        {
                            "error": f"Quantity for Product :{product.title} should be greater than 0"  # noqa
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Check odered product is active or not
                if product.is_active is False:
                    return Response(
                        {"error": f"Product : {product.title} is not active"},  # noqa
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Check ordered product stock is available or not
                if product.stock < quantity:
                    return Response(
                        {
                            "error": f"Product : {product.title} is out of stock or Only {product.stock} stock available now"  # noqa
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    tb_order_item.objects.create(
                        order=order, product=product, quantity=quantity
                    )
                except Exception as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"message": "Order Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            created_order = tb_order.objects.get(id=order.id)
            created_order.delete()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class update_order_status(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = tb_order.objects.get(pk=pk)
            return Response(
                {
                    "message": f"Your Order ID: {order.order_id} status is {order.status.upper()}"
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["packed", "delivered"],
                    },
                },
                "required": ["status"],
            }
        },
        responses={
            200: {"type": "object", "properties": {"message": {"type": "string"}}}
        },
    )
    def put(self, request, pk):

        order_status = request.data.get("status")
        try:
            order = tb_order.objects.get(pk=pk)
            if order_status in status_choices.values:
                order.status = order_status
                order.save()
            if order_status == status_choices.PACKED:
                order_items = tb_order_item.objects.select_related("order").filter(
                    order=order.id
                )
                for item in order_items:
                    if item.product.stock > item.quantity:
                        item.product.stock -= item.quantity
                        item.product.save()
                    else:
                        return Response(
                            {
                                "error": f"Not enough stock for product {item.product.title}"  # noqa
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            return Response({"message": "Status Updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class cancel_order(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            order = tb_order.objects.get(pk=pk)
            if order.can_cancel is True:
                order.status = status_choices.CANCELLED
                order.save()
                return Response(
                    {"message": "Order Cancelled Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": "Order cannot be cancelled now. Your Order Already Packed or Delivered"  # noqa
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
