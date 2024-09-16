from django.db import models

from apartments.models import City


class Attraction(models.Model):
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Отображать в списке'
    )

    city_address_name = models.CharField(
        max_length=256,
        default="Адрес достопримечательности",
        verbose_name="Адрес достопримечательности",
        null=False,
        blank=False
    )
    map_link = models.URLField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Ссылка на карту"
    )
    title = models.CharField(
        max_length=256,
        default="Название достопримечательности",
        verbose_name="Название достопримечательности",
        null=False,
        blank=False
    )
    description = models.TextField(
        max_length=512,
        default="Описание достопримечательности",
        verbose_name="Описание достопримечательности",
        null=False,
        blank=False
    )
    attraction_cite = models.URLField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Сайт достопримечательности"
    )
    time_start = models.TimeField()
    time_end = models.TimeField()

    attraction_logo = models.ImageField()

    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=False, blank=False)

    class Meta:
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'

    def __str__(self):
        return f'{self.city.title}: {self.title}, {self.city_address_name}'
