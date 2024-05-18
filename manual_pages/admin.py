from django.contrib import admin

from manual_pages.models import CleaningChecklistItem, Rules


@admin.register(CleaningChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Пункт уборки квартиры'


@admin.register(Rules)
class RuleAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Правила проживания'
