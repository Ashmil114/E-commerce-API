from rest_framework import serializers
from .models import tb_block_district, tb_block_pincode


class block_district_serializer(serializers.ModelSerializer):
    class Meta:
        model = tb_block_district
        fields = ["id", "district", "reason"]


class block_pincode_serializer(serializers.ModelSerializer):
    class Meta:
        model = tb_block_pincode
        fields = ["id", "pincode", "reason"]
