from django.contrib import admin
from .models import tb_product_subcategory, tb_product_category, tb_product


class admin_product_subcategory(admin.ModelAdmin):
    list_display = ("title", "category")
    list_filter = ("category",)


class admin_product(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "mrp",
        "discount",
        "fixed_quantity",
        "unit",
        "stock",
        "sub_category",
        "seller",
        "is_active",
    )
    list_filter = ("sub_category", "seller")


admin.site.register(tb_product_category)
admin.site.register(tb_product_subcategory, admin_product_subcategory)
admin.site.register(tb_product, admin_product)
