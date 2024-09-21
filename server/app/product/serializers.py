from rest_framework import serializers
from .models import tb_product, tb_product_category, tb_product_subcategory
from app.wishlist.models import tb_wishlist_item
from app.customer.models import tb_customer

# from app.seller.serializers import seller_serializer


class product_category_serializers(serializers.ModelSerializer):
    class Meta:
        model = tb_product_category
        fields = ["id", "title"]
        depth = 1


class product_subcategory_serializers(serializers.ModelSerializer):
    category = product_category_serializers(read_only=True)

    class Meta:
        model = tb_product_subcategory
        fields = ["id", "title", "image", "emoji", "category"]


class product_serializer(serializers.ModelSerializer):
    sub_category = product_subcategory_serializers(read_only=True)
    # seller = seller_serializer()
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = tb_product
        fields = [
            "id",
            "image",
            "title",
            "price",
            "mrp",
            "discount",
            "fixed_quantity",
            "unit",
            "allowed_limit",
            "stock",
            "sub_category",
            "in_wishlist",
            "is_active",
        ]

    def get_in_wishlist(self, obj):
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        if request:
            owner = tb_customer.objects.get(user=request.user)
        return tb_wishlist_item.objects.filter(
            wishlist__owner=owner, product=obj
        ).exists()
