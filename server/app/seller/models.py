from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class tb_shop_category(models.Model):
    name = models.CharField(max_length=200, blank=False, name=False)

    @property
    def get_shops(self):
        return self.shop.all()

    def __str__(self):
        return self.name


class tb_seller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller")
    phone = models.CharField(max_length=10, null=False, blank=False)
    shop_name = models.CharField(max_length=250, null=False, blank=False)
    owner_name = models.CharField(max_length=250, null=False, blank=False)
    category = models.ForeignKey(
        tb_shop_category, on_delete=models.PROTECT, related_name="shop"
    )
    district = models.CharField(max_length=250, null=False, blank=False)
    city = models.CharField(max_length=250, null=False, blank=False)
    pincode = models.CharField(max_length=250, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    @property
    def get_products(self):
        return self.products.all()

    def __str__(self):
        return self.shop_name


@receiver(post_save, sender=tb_seller)
def update_product_is_active(sender, instance, **kwargs):
    if instance.is_active is False:
        for p in instance.get_products:
            p.is_active = False
            p.save()
    else:
        for p in instance.get_products:
            p.is_active = True
            p.save()
