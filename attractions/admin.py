from django.contrib import admin

from attractions.models import Attraction


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    pass
