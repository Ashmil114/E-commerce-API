from rest_framework import serializers
from .models import tb_seller, tb_shop_category


class shop_category_serializers(serializers.ModelSerializer):
    class Meta:
        model = tb_shop_category
        fields = ["id", "name"]
        depth = 1


class seller_serializer(serializers.ModelSerializer):
    category = shop_category_serializers(read_only=True)

    class Meta:
        model = tb_seller
        fields = [
            "id",
            "phone",
            "shop_name",
            "owner_name",
            "category",
            "district",
            "city",
            "pincode",
        ]
