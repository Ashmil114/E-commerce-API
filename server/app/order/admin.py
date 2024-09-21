from django.contrib import admin
from .models import tb_order, tb_order_item


class order_admin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "owner",
        "address",
        "order_date",
        "status",
        "buy_price",
    )


class order_item_admin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "buy_price",
        "buy_total_price",
    )


admin.site.register(tb_order, order_admin)
admin.site.register(tb_order_item, order_item_admin)
