from django.contrib import admin
from .models import tb_shop_category, tb_seller


class admin_seller(admin.ModelAdmin):
    list_display = (
        "shop_name",
        "owner_name",
        "category",
        "district",
        "pincode",
        "is_active",
    )


admin.site.register(tb_seller, admin_seller)
admin.site.register(tb_shop_category)
