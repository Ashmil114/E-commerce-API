from django.contrib import admin
from .models import tb_wishlist, tb_wishlist_item

admin.site.register(tb_wishlist_item)
admin.site.register(tb_wishlist)
