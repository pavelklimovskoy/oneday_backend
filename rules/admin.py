from django.contrib import admin

from rules.models import Rules


@admin.register(Rules)
class RuleAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Правила проживания'

