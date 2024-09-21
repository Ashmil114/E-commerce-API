from rest_framework import serializers
from .models import tb_order, tb_order_item

from app.customer.serializers import address_serializer
from app.product.models import tb_product


class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = tb_product
        fields = ["id", "image", "title", "stock"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class order_item_serializer(serializers.ModelSerializer):
    product = product_serializer()

    class Meta:
        model = tb_order_item
        fields = [
            "product",
            "quantity",
            "buy_price",
            "buy_total_price",
        ]


class orders_serializer(serializers.ModelSerializer):
    items = order_item_serializer(many=True)
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = tb_order
        fields = [
            "id",
            "order_id",
            "order_date",
            "status",
            "buy_price",
            "can_cancel",
            "items",
            "total_quantity",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data = order_item_serializer(
            instance.items.all()[0:3], many=True, context=self.context
        ).data
        representation["items"] = [d["product"]["image"] for d in data]
        return representation

    def get_total_quantity(self, obj):
        return obj.items.all().count()


class order_serializer(serializers.ModelSerializer):
    items = order_item_serializer(many=True)
    address = address_serializer()

    class Meta:
        model = tb_order
        fields = [
            "id",
            "order_id",
            "address",
            "order_date",
            "status",
            "buy_price",
            "can_cancel",
            "items",
        ]
