from rest_framework import serializers
from .models import tb_customer, tb_address


class customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = tb_customer
        fields = ["id", "phone", "name", "email", "on_boarded", "created"]

    def update(self, instance, validated_data):
        instance.on_boarded = True
        return super().update(instance, validated_data)


class address_serializer(serializers.ModelSerializer):
    class Meta:
        model = tb_address
        fields = [
            "id",
            "name",
            "phone",
            "alt_phone",
            "city_or_town",
            "pin",
            "district",
            "landmark",
        ]
