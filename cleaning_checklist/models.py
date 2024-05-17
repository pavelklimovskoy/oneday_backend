from django.db import models
from django.db.models.fields import TextField

from infrastructure.models import OrderFieldModel


class CleaningChecklistItem(OrderFieldModel):
    item_text: TextField = models.TextField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Текст пункта",
    )

