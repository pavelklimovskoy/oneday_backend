from django.db import models


class City(models.Model):
    real_calendar_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

    map_longitude = models.CharField(
        max_length=100,
        default=None,
        null=True,
        blank=True
    )
    map_latitude = models.CharField(
        max_length=100,
        default=None,
        null=True,
        blank=True
    )
    map_view_zoom = models.IntegerField(
        default=15,
    )

    def __str__(self):
        return f'Город: {self.title} id:{self.real_calendar_id}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class ApartmentService(models.Model):
    service_name = models.CharField(max_length=100)
    service_title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.service_title} title:{self.service_name}'

    class Meta:
        verbose_name = 'Удобство'
        verbose_name_plural = 'Удобства'


class Apartment(models.Model):
    real_calendar_id = models.IntegerField()
    address = models.CharField(max_length=512)
    rooms = models.IntegerField()
    sleeps = models.CharField(max_length=512)
    desc = models.TextField()
    floor = models.IntegerField(null=True, blank=True, default=0)
    humans = models.IntegerField()
    title = models.CharField(max_length=512)
    price = models.IntegerField()

    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    services = models.ManyToManyField(ApartmentService, related_name='services')

    map_longitude = models.FloatField(null=True, blank=True, default=None)
    map_latitude = models.FloatField(null=True, blank=True, default=None)

    main_photo = models.URLField(null=True, blank=True, default=None)

    area = models.IntegerField(
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title} {self.address}'

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'


class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='photos', on_delete=models.CASCADE)
    photo_url = models.URLField(max_length=512)

    def __str__(self):
        return f'{self.apartment.title} {self.photo_url}'

    class Meta:
        verbose_name = 'Фото квартиры'
        verbose_name_plural = 'Фото квартир'
