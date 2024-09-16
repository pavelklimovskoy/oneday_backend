from django.contrib import admin

from apartments.models import Apartment, ApartmentService, City, ApartmentPhoto


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Квартира'


@admin.register(ApartmentService)
class ApartmentServiceAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Удобства'


@admin.register(ApartmentPhoto)
class ApartmentPhotoAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Фотография квартиры'
        verbose_name_plural = 'Фотографии квартир'
