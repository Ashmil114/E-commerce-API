from django.db import models
import uuid


class tb_block_district(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.CharField(max_length=250, null=False, blank=False)
    reason = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.district = self.district.lower()
        super(tb_block_district, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.district} Blocked"


class tb_block_pincode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pincode = models.CharField(max_length=250, null=False, blank=False)
    reason = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pincode} Blocked"
