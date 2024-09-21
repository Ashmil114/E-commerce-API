from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class tb_customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer", editable=False
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False,
        editable=False,
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        blank=True,
        null=True,
    )
    on_boarded = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def get_address(self):
        return self.addresses.all()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.phone


class tb_otp(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="otp", editable=False
    )
    otp = models.CharField(max_length=4, null=True, blank=True)
    number_of_time_try_to_otp = models.IntegerField(default=0)
    last_otp_attempt = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    def __str__(self):
        return self.user.username


class tb_address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        tb_customer,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    phone = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )
    alt_phone = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    city_or_town = models.CharField(max_length=250, null=False, blank=False)
    pin = models.CharField(max_length=250, null=False, blank=False)
    district = models.CharField(max_length=250, null=False, blank=False)
    landmark = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} Address"
