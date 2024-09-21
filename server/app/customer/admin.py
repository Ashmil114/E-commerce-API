from django.contrib import admin
from .models import tb_customer, tb_otp, tb_address

admin.site.register(tb_customer)
admin.site.register(tb_otp)
admin.site.register(tb_address)
