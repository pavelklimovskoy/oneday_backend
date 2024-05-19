from django.contrib import admin

from analytics.models import BookingAnalytics


@admin.register(BookingAnalytics)
class BookingAnalyticsAdmin(admin.ModelAdmin):

    # readonly_fields = ('*')
    class Meta:
        verbose_name = 'Записи о бронировании'
        verbose_name_plural = 'Запись о бронировании'
