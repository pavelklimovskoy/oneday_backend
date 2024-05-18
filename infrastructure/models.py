from django.db import models
from django.db.models.fields import PositiveIntegerField


class OrderFieldModel(models.Model):
    order: PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="order",
        editable=True,
        db_index=True,
        default=0
    )

    class Meta:
        abstract = True
        ordering = ("order",)
