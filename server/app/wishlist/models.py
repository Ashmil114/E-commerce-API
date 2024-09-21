from django.db import models
import uuid
from app.customer.models import tb_customer
from app.product.models import tb_product


class tb_wishlist_item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(tb_product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title


class tb_wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    owner = models.ForeignKey(
        tb_customer,
        on_delete=models.CASCADE,
        related_name="wishlist",
        null=True,
        blank=True,
    )
    items = models.ManyToManyField(
        tb_wishlist_item, related_name="wishlist", blank=True
    )
    district = models.CharField(max_length=250, null=True, blank=True)
    is_for_everyone = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.owner:
            self.is_for_everyone = True
        else:
            self.is_for_everyone = False
        super(tb_wishlist, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
