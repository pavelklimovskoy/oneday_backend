# coding:utf-8

from django.db import models
from django.db.models import BooleanField
from django.db.models.fields import TextField, PositiveIntegerField
from django.forms import CharField


class CleaningChecklistItem(models.Model):
    item_name: CharField = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default='Название по умолчанию',
        verbose_name='Название пункта'
    )
    item_text: TextField = models.TextField(
        max_length=200,
        null=False,
        blank=False,
        default='Текст пункта уборки',
        verbose_name="Текст пункта",
    )
    is_visible: BooleanField = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name='Отображать в списке'
    )

    order: PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="order",
        editable=True,
        db_index=True,
        default=0
    )

    def __str__(self) -> str:
        visible_verdict: str = "Отображается"
        if not self.is_visible:
            visible_verdict: str = "Скрыт"
        return f'Правило проживания №{self.order} {self.item_name} {visible_verdict}'

    class Meta:
        ordering = ("order",)
        verbose_name = 'Пункты уборки'
        verbose_name_plural = 'Пункт уборки'


class Rules(models.Model):
    rules_name: CharField = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default='Название по умолчанию',
        verbose_name='Название правила'
    )
    rules_text: TextField = models.TextField(
        max_length=1000,
        null=False,
        blank=False,
        default='Текст правила проживания',
        verbose_name='Текст правила'
    )
    is_visible: BooleanField = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name='Отображать в списке'
    )

    order: PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="order",
        editable=True,
        db_index=True,
        default=0
    )

    def __str__(self) -> str:
        visible_verdict: str = "Отображается"
        if not self.is_visible:
            visible_verdict: str = "Скрыт"
        return f'Правило проживания №{self.order} {self.rules_name} {visible_verdict}'

    class Meta:
        ordering = ("order",)
        verbose_name = 'Правило проживания'
        verbose_name_plural = 'Правила проживания'
