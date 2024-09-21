from rest_framework import serializers
from .models import tb_wishlist, tb_wishlist_item
from app.product.models import tb_product


class product_serializer(serializers.ModelSerializer):

    class Meta:
        model = tb_product
        fields = [
            "id",
            "image",
            "title",
            "price",
            "unit",
        ]

    # For Get Full Image urls
    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class wishlist_item_serializer(serializers.ModelSerializer):
    product = product_serializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = tb_wishlist_item
        fields = [
            "id",
            "product",
            "quantity",
            "total_price",
        ]
        depth = 1

    def get_total_price(self, obj):
        return obj.total_price()


class wishlist_serializer(serializers.ModelSerializer):
    items = wishlist_item_serializer(read_only=True, many=True)
    number_of_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = tb_wishlist
        fields = [
            "id",
            "title",
            "items",
            "number_of_items",
            "total_price",
        ]
        depth = 2

    def get_number_of_items(self, obj):
        return obj.items.count()

    def get_total_price(self, obj):
        return sum(item.total_price() for item in obj.items.all())
