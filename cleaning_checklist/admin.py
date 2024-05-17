from django.contrib import admin

from cleaning_checklist.models import CleaningChecklistItem


@admin.register(CleaningChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Пункт уборки квартиры'

