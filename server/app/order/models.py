from django.db import models
import uuid
from datetime import datetime
from app.customer.models import tb_customer, tb_address
from app.product.models import tb_product


class status_choices(models.TextChoices):
    PROCESSING = ("processing", "Processing")
    PACKED = ("packed", "Packed")
    DELIVERED = ("delivered", "Delivered")
    CANCELLED = ("cancelled", "Cancelled")


class tb_order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    owner = models.ForeignKey(
        tb_customer,
        on_delete=models.CASCADE,
        related_name="orders",
        null=False,
        blank=False,
    )
    address = models.ForeignKey(
        tb_address,
        on_delete=models.CASCADE,
        related_name="orders",
        null=False,
        blank=False,
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=250,
        choices=status_choices.choices,
        default=status_choices.PROCESSING,
    )
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    can_cancel = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.order_id:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = uuid.uuid4().hex[:6].upper()
            self.order_id = f"OD{timestamp}{unique_id}"
        if self.status == status_choices.PROCESSING:
            self.can_cancel = True
        else:
            self.can_cancel = False
        super(tb_order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.owner.name}"


class tb_order_item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(tb_order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(tb_product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    buy_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    buy_total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.buy_price:
            self.buy_price = self.product.price
        if not self.buy_total_price:
            self.buy_total_price = self.buy_price * self.quantity

        super(tb_order_item, self).save(*args, **kwargs)
        self.order.buy_price = sum(
            item.product.price * item.quantity for item in self.order.items.all()
        )
        self.order.save()

    def __str__(self):
        return self.order.order_id
