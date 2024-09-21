from django.db import models
import uuid
import os
from server.storage import OverwriteStorage
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .covert_webp import convert_image_to_webp


from app.seller.models import tb_seller


class tb_product_category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)

    @property
    def get_subcategories(self):
        return self.subcategories.all()

    def __str__(self):
        return self.title


def subcategory_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return f"product/category/{instance.id}{extension}"


class tb_product_subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    image = models.ImageField(
        upload_to=subcategory_image_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True,
    )
    emoji = models.CharField(max_length=250, blank=True, null=True, default="🛒")
    category = models.ForeignKey(
        tb_product_category, on_delete=models.PROTECT, related_name="subcategories"
    )

    @property
    def get_products(self):
        return self.products.all()

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=tb_product_subcategory)
def delete_product_subcategory_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=tb_product_subcategory)
def do(sender, instance, **kwargs):
    convert_image_to_webp(sender, instance, **kwargs)


def product_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return f"product/image/{instance.id}{extension}"


class active_product_manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class tb_product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to=product_image_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True,
    )
    title = models.TextField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    mrp = models.IntegerField(blank=False, null=False, default=0)
    discount = models.IntegerField(blank=True, null=True)
    fixed_quantity = models.IntegerField(blank=False, null=False, default=0)
    unit = models.CharField(max_length=50, null=False, blank=False)
    allowed_limit = models.IntegerField(blank=False, null=False, default=1)
    stock = models.IntegerField(blank=False, null=False)
    sub_category = models.ForeignKey(
        tb_product_subcategory,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="products",
    )
    seller = models.ForeignKey(
        tb_seller,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="products",
    )
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.mrp > 0:
            self.discount = int(((self.mrp - self.price) / self.mrp) * 100)
        else:
            self.discount = 0
        if self.seller.is_active is False:
            self.is_active = False
        else:
            if self.stock == 0:
                self.is_active = False
            else:
                self.is_active = True

        super(tb_product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


@receiver(post_delete, sender=tb_product)
def delete_product_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=tb_product)
def do_product_img_convertion(sender, instance, **kwargs):
    convert_image_to_webp(sender, instance, **kwargs)
